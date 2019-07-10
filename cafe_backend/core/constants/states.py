class DEFAULT_STATE(object):
    approved = 'a'
    blank = 'b'
    canceled = 'c'
    default = 'd'
    delivered = 'e'
    draft = 'f'
    in_progress = 'g'
    initial = 'i'
    rejected = 'r'
    pending = 'p'
    using = 'u'
    waiting = 'w'
    archived = 'x'


class ORDER_STATE:
    default = DEFAULT_STATE.default
    canceled = DEFAULT_STATE.canceled
    delivered = DEFAULT_STATE.delivered
    archived = DEFAULT_STATE.archived


class BOOKING_STATE:
    default = DEFAULT_STATE.default
    approved = DEFAULT_STATE.approved
    rejected = DEFAULT_STATE.rejected
    canceled = DEFAULT_STATE.canceled
    archived = DEFAULT_STATE.archived


class TABLE_STATE:
    blank = DEFAULT_STATE.blank
    using = DEFAULT_STATE.using
    reserved = DEFAULT_STATE.rejected
    # waiting = DEFAULT_STATE.waiting


class MUSIC_STATE:
    default = DEFAULT_STATE.default
    downloading = DEFAULT_STATE.pending
    uploading = DEFAULT_STATE.in_progress
    ready = DEFAULT_STATE.approved
