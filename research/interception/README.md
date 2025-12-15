# Перехват трафика kwork (рабочая процедура)

Проверено на Redmi Note 7 (lavender), Android 13, root (Magisk), adb `276bcca9`.
SSL pinning у приложения **нет** — Frida не нужен, достаточно системного CA.

Соединение с устройством — через USB (`adb reverse`), общая Wi-Fi сеть не требуется.

## Подготовка CA (один раз)

```bash
CA=~/.mitmproxy/mitmproxy-ca-cert.pem            # создаётся при первом запуске mitmproxy
HASH=$(openssl x509 -inform PEM -subject_hash_old -in "$CA" | head -1)
cp "$CA" research/interception/$HASH.0           # .0 в .gitignore
```

## Старт перехвата

```bash
# 1. CA в системное хранилище (tmpfs bind-mount, до перезагрузки, /system не трогаем)
adb -s 276bcca9 push research/interception/$HASH.0 /data/local/tmp/$HASH.0
adb -s 276bcca9 shell 'su -c "mkdir -p /data/local/tmp/cc && cp /system/etc/security/cacerts/* /data/local/tmp/cc/ && mount -t tmpfs tmpfs /system/etc/security/cacerts && cp /data/local/tmp/cc/* /system/etc/security/cacerts/ && cp /data/local/tmp/'$HASH'.0 /system/etc/security/cacerts/ && chmod 644 /system/etc/security/cacerts/* && chcon u:object_r:system_security_cacerts_file:s0 /system/etc/security/cacerts/*"'

# 2. USB-туннель device:8080 -> PC:8080 + системный прокси
adb -s 276bcca9 reverse tcp:8080 tcp:8080
adb -s 276bcca9 shell settings put global http_proxy 127.0.0.1:8080

# 3. mitmdump с аддоном (пишет api.kwork.* в captures/kwork_flows.jsonl)
mitmdump --listen-port 8080 -s research/interception/capture_addon.py -w research/captures/kwork.flows "~d kwork"

# 4. перезапустить приложение, чтобы подхватило прокси
adb -s 276bcca9 shell am force-stop ru.kwork.app
adb -s 276bcca9 shell monkey -p ru.kwork.app -c android.intent.category.LAUNCHER 1
```

Дальше «протыкать» нужные экраны в приложении — флоу копятся в `research/captures/`.

## Остановка и восстановление устройства

```bash
adb -s 276bcca9 shell settings delete global http_proxy
adb -s 276bcca9 reverse --remove-all
adb -s 276bcca9 shell 'su -c "umount /system/etc/security/cacerts; rm -rf /data/local/tmp/cc /data/local/tmp/'$HASH'.0"'
pkill -f 'mitmdump --listen-port 8080'
```

## Анализ

```bash
python research/build_schemas.py > docs/06-captured-responses.md   # схемы ответов (санитизировано)
```

> ⚠️ `research/captures/` и `research/interception/*.0` — в `.gitignore`: содержат
> личные данные, токены и сертификат. В репозиторий не коммитятся.
