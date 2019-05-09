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
