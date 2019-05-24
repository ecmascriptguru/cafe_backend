class DEFAULT_MEDIA_TYPE:
    text = 't'
    music = 'm'
    video = 'v'
    image = 'i'


class ADS_TYPE:
    image = DEFAULT_MEDIA_TYPE.image
    video = DEFAULT_MEDIA_TYPE.video


class EVENT_TYPE:
    image = DEFAULT_MEDIA_TYPE.image
    video = DEFAULT_MEDIA_TYPE.video


class EVENT_REPEAT_TYPE:
    only_once = 'o'
    every_day = 'd'
    every_week = 'w'


class CHAT_ROOM_TYPE:
    direct = 'd'
    private = 'c'
    public = 'p'


class SOCKET_MESSAGE_TYPE:
    chat = 'chat_message'
    event = 'notification_event'
    order = 'notification_order'
    order_item = 'notification_order_item'
    table = 'notification_table'
    qr_code = 'qr_code'
    ring = 'ring'
