# Фаза 1 — Разведка: захват трафика мобильного приложения kwork

Цель: получить реальные эндпоинты `api.kwork.ru`, статичный `Authorization`-токен
приложения, User-Agent и форму ответов. Результат заносится в
[`endpoints.md`](endpoints.md), по нему достраивается библиотека.

> Устройство: **Redmi Note 7 (lavender), root**, adb-serial `276bcca9`.

## Инструменты

```bash
# на ПК (Arch/CachyOS)
sudo pacman -S android-tools mitmproxy   # adb + mitmproxy
yay -S jadx                              # декомпилятор APK (или scoop/официальный релиз)
pip install frida-tools                  # обход SSL pinning (опционально)
```

## Шаг 1. Вытащить APK и декомпилировать

```bash
# найти пакет (обычно ru.kwork.android или похоже)
adb -s 276bcca9 shell pm list packages | grep -i kwork
# путь к APK
adb -s 276bcca9 shell pm path <package>
# скачать
adb -s 276bcca9 pull <path>/base.apk research/captures/kwork.apk
# декомпилировать в исходники Java
jadx -d research/captures/kwork-src research/captures/kwork.apk
```

Что искать в `kwork-src`:
- базовый URL (`api.kwork.ru`), пути методов;
- статичный заголовок `Authorization: Basic <...>` (часто в Retrofit/OkHttp
  interceptor или в BuildConfig);
- User-Agent;
- наличие подписи запросов (HMAC/секрет) — если есть, фиксируем алгоритм.

## Шаг 2. Поднять mitmproxy и завернуть трафик устройства

```bash
mitmweb --listen-port 8080            # web-интерфейс на http://127.0.0.1:8081
```

На устройстве (root) ставим CA mitmproxy в СИСТЕМНЫЕ сертификаты (с Android 7+
пользовательские CA не доверяются трафиком приложений):

```bash
# сертификат генерится при первом запуске mitmproxy в ~/.mitmproxy/
HASH=$(openssl x509 -inform PEM -subject_hash_old -in ~/.mitmproxy/mitmproxy-ca-cert.pem | head -1)
cp ~/.mitmproxy/mitmproxy-ca-cert.pem /tmp/$HASH.0
adb -s 276bcca9 root && adb -s 276bcca9 remount
adb -s 276bcca9 push /tmp/$HASH.0 /system/etc/security/cacerts/
adb -s 276bcca9 shell chmod 644 /system/etc/security/cacerts/$HASH.0
adb -s 276bcca9 reboot
```

Направить трафик устройства на ПК (ПК и телефон в одной сети):
- Settings → Wi-Fi → прокси: вручную, host = IP ПК, port = 8080.

## Шаг 3. Обход SSL pinning (если приложение не подключается)

```bash
# залить и запустить frida-server (под архитектуру устройства, lavender = arm64)
adb -s 276bcca9 push frida-server /data/local/tmp/
adb -s 276bcca9 shell "chmod 755 /data/local/tmp/frida-server && /data/local/tmp/frida-server &"
# на ПК — universal unpinning
frida -U -f <package> -l ssl-unpinning.js
```

## Шаг 4. Снять сценарии и задокументировать

Пройти в приложении сценарии: вход, открытие каталога/поиска, лента биржи проектов,
заказы, диалоги/отправка сообщения, экран настроек. Каждый запрос из mitmproxy
сохранить (Export → flow/HAR в `research/captures/`, они в .gitignore) и описать в
[`endpoints.md`](endpoints.md): метод, URL, поля запроса, пример ответа.

> ⚠️ В `captures/` попадают логин-токены и личные данные — каталог в `.gitignore`,
> не коммитить.
