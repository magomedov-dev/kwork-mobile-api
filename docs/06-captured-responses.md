# Справочник ответов API (по живому трафику)

> Санитизировано: только имена полей и типы, без реальных значений. Источник — 2 прогона приложения через mitmproxy (895 flows). Общие поля запроса (`token`, `uad`, `slrememberme`, `device`) опущены.

Подтверждено эндпоинтов с телом ответа: **63**.


## `POST /actor`

**Поля запроса:** `isAppWhiteListed`, `whiteListedLastShowTime`, `whiteListedWindowSkipped`, `isAppPushOn`, `appPushOnLastShowTime`, `makeOnline`

**Схема ответа:**

```
success: bool
response:
  id: int
  username: str
  status: str
  email: str
  type: str
  verified: bool
  profilepicture: str
  description: str
  slogan: str
  fullname: str
  level_description: str
  cover: str
  good_reviews: int
  bad_reviews: int
  location: str
  rating: str
  rating_count: int
  hold_amount: int
  free_amount: int
  currency: str
  inbox_archive_count: int
  unread_dialog_count: int
  notify_unread_count: int
  red_notify: bool
  warning_inbox_count: int
  app_notify_count: int
  unread_messages_count: int
  country_id: int
  city_id: int
  timezone_id: int
  addtime: int
  allow_mobile_push: bool
  is_more_payer: bool
  kworks_count: int
  favourite_kworks_count: int
  hidden_kworks_count: int
  specialization: null
  profession: null
  kworks_available_at_weekends: bool
  achievments_list:
    - [список]:
      id: int
      name: str
      description: str
      image_url: str
fcmTokenLost: bool
```

## `POST /allowMobilePush`

**Поля запроса:** `allow`

**Схема ответа:**

```
success: bool
```

## `POST /api/file/upload`

**Поля запроса:** `<multipart>`

**Схема ответа:**

```
result: str
file_id: int
file_name: str
file_path: str
file_path_hash: str
file_extension: str
need_miniature: bool
```

## `POST /api/offer/createoffer`

**Поля запроса:** `<multipart>`

**Схема ответа:**

```
success: bool
data: null
redirect: str
```

## `POST /api/offer/deleteoffer`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
```

## `POST /api/offer/editoffer`

**Поля запроса:** `<multipart>`

**Схема ответа:**

```
success: bool
data: null
redirect: str
```

## `POST /api/validation/checktext`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data:
  description:
    mistakes:
      - [список]:
        - [список]:
          int
    validError: str
    mistakesPercentExceeded: bool
```

## `POST /blockDialog`

**Поля запроса:** `blockUserId`

**Схема ответа:**

```
success: bool
response:
  message: str
```

## `POST /blockedDialogs`

**Поля запроса:** `page`

**Схема ответа:**

```
success: bool
response: []
paging:
  page: int
  total: int
  limit: int
```

## `POST /catalogFilters`

**Поля запроса:** `categoryId`, `classifierId`

**Схема ответа:**

```
success: bool
response:
  filters:
    - [список]:
      name: str
      type: str
      id: int
      mobile_group_id: int
      is_package: int
      values:
        - [список]:
          object
  groups:
    - [список]:
      id: int
      name: str
  kworks_count: int
```

## `POST /exchangeInfo`

**Поля запроса:** `—`

**Схема ответа:**

```
archived_count: int
exchange_response_count: int
```

## `POST /favoriteCategories`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    id: int
    name: str
    description: str
    is_attribute: bool
```

## `POST /favoriteKworks`

**Поля запроса:** `page`

**Схема ответа:**

```
success: bool
response: []
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /getAvailableFeatures`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
  voice_messages:
    is_voice_message_recording_available: bool
    speed_control:
      is_available: bool
      speed: int
      available_speeds:
        - [список]:
          int
    receiving_settings:
      should_show_settings_popup: bool
      is_receiving_setting_allowed: bool
      is_receiving_allowed: bool
  features:
    is_exchange_available: bool
    vat_rate_blocking:
      should_show: bool
  is_support_dialog_available: bool
  test_groups:
    mobile_android_seller_payout_explainer: bool
    mobile_android_pagination: bool
    mobile_android_preview_status: bool
    mobile_android_check_internet: bool
    mobile_android_balance_cancel: bool
    mobile_android_fcm_event_validation: bool
    mobile_android_migrate_to_yescrow: bool
```

## `POST /getBadgesInfo`

**Поля запроса:** `makeOnline`

**Схема ответа:**

```
success: bool
response:
  dialogs_unread_count: int
  notifications_unread_count: int
  important_notifications_count: bool
  warning_dialogs_count: int
  unread_messages_count: int
  notifications_not_delivered: bool
  important_dialog_count: int
```

## `POST /getChannel`

**Поля запроса:** `makeOnline`

**Схема ответа:**

```
success: bool
response:
  channel: str
```

## `POST /getDialog`

**Поля запроса:** `id`, `makeOnline`, `withTracks`

**Схема ответа:**

```
success: bool
response:
  unread: bool
  unread_count: int
  last_message: str
  time: int
  user_id: int
  username: str
  profilepicture: str
  is_online: bool
  lastOnlineTime: int
  link: str
  status: str
  blocked_by_user: bool
  allowedDialog: bool
  lastMessage:
    unread: bool
    fromUsername: str
    fromUserId: int
    type: str
    time: int
    message: str
    profilePicture: str
    originText: str
  has_active_order: bool
  archived: bool
  isStarred: bool
  warning_message_id: int
  countup: int
  has_answer: bool
  is_allow_custom_request: bool
  hidden_at: int
  is_important: bool
  moderation_status: null
  draft: str
  is_stop_work: null
  disallowReason: int
  active_orders: []
  is_voice_message_blocked: bool
```

## `POST /getInAppNotification`

**Поля запроса:** `app_version`, `os_type`, `os_version`

**Схема ответа:**

```
success: bool
response: null
```

## `POST /getInboxTracks`

**Поля запроса:** `userId`, `limit`, `direction`, `makeOnline`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    conversation_id: int
    entity_type: int
    message_id: int
    to_id: int
    to_username: str
    to_live_date: int
    from_id: int
    from_username: str
    from_live_date: int
    from_profilepicture: str
    to_profilepicture: str
    manager_name: str
    message: str
    time: int
    unread: bool
    type: null
    status: str
    created_order_id: null
    forwarded: bool
    updated_at: null
    warning_type: str
    countup: int
    message_page: int
    message_key: null
paging:
  page: int
  pages: int
  total: int
  limit: int
extra:
  hasRemovedMessages: bool
user:
  user_id: int
  username: str
  last_online_timestamp: int
  avatar_image_path: str
orders: []
```

## `POST /getPaymentMethods`

**Поля запроса:** `withCompany`

**Схема ответа:**

```
success: bool
response:
  service_fee_type: str
  service_fee_min: int
  service_fee_percent: int
  service_fee_min_percent_sum: int
  service_fee_fixed: int
  payment_type_available_collection:
    - [список]:
      type: str
      name: str
      country_group_code: str
      amount_limits: null
      lock_refill_sum: bool
  currency: str
  service_fee_percent_levels:
    - [список]:
      from: int
      percent: float
```

## `POST /getPublicFeatures`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
```

## `POST /getSecurityUserData`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
  email: str
  username: str
  username_changed: bool
  phone: str
  confirmation_type: str
  is_available_kwork_creation: bool
  username_change_available: null
  is_profile_completed:
    details: bool
    profession: bool
    profile_pic: bool
  whatsapp_link: str
  telegram_bot_link: str
```

## `POST /getWantsCount`

**Поля запроса:** `attributes`

**Схема ответа:**

```
success: bool
response:
  count: int
  filters:
    by_budget:
      - [список]:
        object
    offers:
      - [список]:
        object
```

## `POST /getWebAuthToken`

**Поля запроса:** `url_to_redirect`

**Схема ответа:**

```
success: bool
response:
  token: str
  expires_at: int
  url: str
  url_to_redirect: str
```

## `POST /hideDialog`

**Поля запроса:** `userId`, `isRestore`

**Схема ответа:**

```
success: bool
response:
  message: str
  unhide_available_secs: int
```

## `POST /inboxCreate`

**Поля запроса:** `user_id`, `message_key`, `text`

**Схема ответа:**

```
success: bool
response:
  id: int
  conversation_id: int
  type: str
  page: int
  time: int
  mass_mailing_notification: bool
```

## `POST /inboxRead`

**Поля запроса:** `user_id`

**Схема ответа:**

```
success: bool
```

## `POST /isDialogAllow`

**Поля запроса:** `receiverId`

**Схема ответа:**

```
success: bool
response:
  privateMessageStatuses:
    default: int
    conversationTime: int
    orderTime: int
    orderCancel: int
    orderRating: int
    support: int
    userBlockedTemporarily: int
    userBlockedPermanently: int
    blocked_by_receiver: int
    blocked_by_sender: int
    blocked_by_both: int
    spamer: int
    userIsViewedProjects: int
    interlocutorIsDeleted: int
    oldConversation: int
    showFishingTutorial: int
    conversationLongTime: int
    currentUserBlocked: int
    sellerOnboardingRequired: int
  privateMessageStatus: int
  showInboxAllowModal: int
  isPageNeedSmsVerification: int
  isOnline: int
  currentUserTime: int
  isDaytime: int
  hasDialog: bool
  utcOffset: int
  userUtcOffset: int
  sellerIsNotAvailable: bool
  receivedLastOnline: int
  isSmsVerified: int
```

## `POST /kworks`

**Поля запроса:** `categoryId`, `classifierId`, `packages[0][id]`, `packages[0][value]`, `packages[1][id]`, `packages[1][value]`, `price`, `sdeliverytime`, `sellerlvl`, `sonline`, `sminreview`, `sordersqueue`, `sview`, `strack`, `page`, `limit`

**Схема ответа:**

```
success: bool
response:
  kworks_count: int
  kworks: []
  classifiers:
    - [список]:
      id: int
      name: str
      kworks_count: int
      visibility: int
  paging:
    pages: int
    page: int
    total: int
    limit: int
```

## `POST /kworksStatusList`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    id: int
    name: str
    kworks_count: int
    kworks: []
```

## `POST /myWants`

**Поля запроса:** `page`, `want_status_id`

**Схема ответа:**

```
success: bool
response: []
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /notifications`

**Поля запроса:** `makeOnline`

**Схема ответа:**

```
success: bool
```

## `POST /notificationsFetch`

**Поля запроса:** `page`, `makeOnline`

**Схема ответа:**

```
success: bool
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /offline`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
```

## `POST /payerOrders`

**Поля запроса:** `filter`, `company_orders`

**Схема ответа:**

```
success: bool
error: str
error_code: int
```

## `POST /projects`

**Поля запроса:** `categories`, `price_to`, `page`

**Схема ответа:**

```
success: bool
connects:
  all_connects: int
  active_connects: int
  update_time: int
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /projects/check_is_template`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data: []
```

## `POST /rechargeBalance`

**Поля запроса:** `orderId`, `amount`, `payment_id`, `paymentType`, `country_group_code`

**Схема ответа:**

```
success: bool
response:
  paymentUrlWebView: str
```

## `POST /registerCloudToken`

**Поля запроса:** `cloud_token`, `os`, `os_version`, `app_version`

**Схема ответа:**

```
success: bool
```

## `POST /searchDialogs`

**Поля запроса:** `query`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    unread: bool
    unread_count: int
    last_message: str
    time: int
    user_id: int
    username: str
    profilepicture: str
    is_online: bool
    lastOnlineTime: int
    link: str
    status: str
    blocked_by_user: bool
    allowedDialog: bool
    lastMessage:
      unread: bool
      fromUsername: str
      fromUserId: int
      type: str
      time: int
      message: str
      profilePicture: str
      originText: str
    has_active_order: bool
    archived: bool
    isStarred: bool
    warning_message_id: int
    countup: int
    has_answer: bool
    is_allow_custom_request: bool
    hidden_at: int
    is_important: bool
    moderation_status: null
    draft: str
    is_stop_work: null
    disallowReason: int
    active_orders: []
    not_available_for_company: bool
paging:
  page: int
  total: int
  limit: str
```

## `POST /searchInboxes`

**Поля запроса:** `query`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    message_id: int
    to_id: int
    to_username: str
    to_live_date: str
    from_id: int
    from_username: str
    from_live_date: str
    from_profilepicture: str
    to_profilepicture: str
    manager_name: str
    message: str
    time: int
    unread: bool
    type: null
    status: str
    created_order_id: null
    forwarded: bool
    updated_at: null
    warning_type: null
    countup: int
    conversation_id: int
    message_page: int
paging:
  page: int
  pages: int
  total: int
  limit: int
```

## `POST /searchKworksCatalogQuery`

**Поля запроса:** `page`

**Схема ответа:**

```
success: bool
response: []
```

## `POST /searchMessages`

**Поля запроса:** `text`, `userId`, `page`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    id: int
    conversation_id: int
    phrase: str
paging:
  page: int
  pages: int
  total: int
  limit: int
```

## `POST /sendUserStatus`

**Поля запроса:** `user_id`, `status`

**Схема ответа:**

```
success: bool
```

## `POST /setDialogStarred`

**Поля запроса:** `userId`, `isStarred`

**Схема ответа:**

```
success: bool
response:
  message: str
```

## `POST /setFavorite`

**Поля запроса:** `attributes`

**Схема ответа:**

```
success: bool
```

## `POST /setUserType`

**Поля запроса:** `type`

**Схема ответа:**

```
success: bool
response:
  voice_messages:
    is_voice_message_recording_available: bool
    speed_control:
      is_available: bool
      speed: int
      available_speeds:
        - [список]:
          int
    receiving_settings:
      should_show_settings_popup: bool
      is_receiving_setting_allowed: bool
      is_receiving_allowed: bool
  features:
    is_exchange_available: bool
    vat_rate_blocking:
      should_show: bool
  is_support_dialog_available: bool
  test_groups:
    mobile_android_seller_payout_explainer: bool
    mobile_android_pagination: bool
    mobile_android_preview_status: bool
    mobile_android_check_internet: bool
    mobile_android_balance_cancel: bool
    mobile_android_fcm_event_validation: bool
    mobile_android_migrate_to_yescrow: bool
```

## `POST /signIn`

**Поля запроса:** `login`

**Схема ответа:**

```
success: bool
response:
  token: str
  expired: int
  need_2fa: bool
```

## `POST /timezones`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response:
  - [список]:
    id: int
    utc_offset: int
    name: str
```

## `POST /unblockDialog`

**Поля запроса:** `blockUserId`

**Схема ответа:**

```
success: bool
response:
  message: str
```

## `POST /unreadDialog`

**Поля запроса:** `user_id`

**Схема ответа:**

```
success: bool
```

## `POST /updateSettings`

**Поля запроса:** `username`, `fullname`, `timezoneId`, `email`, `countryId`, `cityId`, `details`, `profession`

**Схема ответа:**

```
success: bool
response:
  message: str
```

## `POST /user`

**Поля запроса:** `id`, `makeOnline`

**Схема ответа:**

```
success: bool
response:
  id: int
  username: str
  status: str
  fullname: str
  profilepicture: str
  description: str
  slogan: str
  location: str
  rating: str
  rating_count: int
  level_description: str
  good_reviews: int
  bad_reviews: int
  reviews_count: int
  online: bool
  live_date: int
  cover: str
  custom_request_min_budget: int
  is_allow_custom_request: bool
  order_done_persent: int
  order_done_intime_persent: int
  order_done_repeat_persent: int
  timezoneId: int
  blocked_by_user: bool
  allowedDialog: bool
  addtime: int
  achievments_list:
    - [список]:
      id: int
      name: str
      description: str
      image_url: str
  completed_orders_count: int
  specialization: null
  profession: null
  kworks_count: int
  kworks: []
  portfolio_list: null
  reviews: null
  skills: []
  is_verified_worker: bool
  note: []
  is_cashless_payment_available: bool
  is_stop_work: null
```

## `POST /userReviews`

**Поля запроса:** `user_id`, `type`, `page`

**Схема ответа:**

```
success: bool
response: []
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /user_online`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data: null
```

## `POST /viewedCatalogKworks`

**Поля запроса:** `page`

**Схема ответа:**

```
success: bool
paging:
  page: int
  total: int
  limit: int
  pages: int
```

## `POST /wants/create_offer_draft`

**Поля запроса:** `<multipart>`

**Схема ответа:**

```
success: bool
data: null
```

## `POST /wants/create_want_draft`

**Поля запроса:** `<multipart>`

**Схема ответа:**

```
success: bool
data: null
```

## `POST /wants/get_category_hints`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data: null
```

## `POST /wants/loadclassification`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data:
  1187: str
  1188: str
```

## `POST /wants/portfolio`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
data:
  totalCount: int
  offset: int
  curCount: int
  haveNext: int
  portfolioJson: []
  allPortfolioIds: []
```

## `POST /wantsStatusList`

**Поля запроса:** `—`

**Схема ответа:**

```
success: bool
response: []
```

## `POST /workerOrders`

**Поля запроса:** `filter`

**Схема ответа:**

```
success: bool
error: str
error_code: int
```
