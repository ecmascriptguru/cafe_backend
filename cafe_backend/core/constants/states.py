class DEFAULT_STATE(object):
    approved = 'a'
    canceled = 'c'
    default = 'd'
    delivered = 'e'
    draft = 'f'
    in_progress = 'g'
    initial = 'i'
    rejected = 'r'
    pending = 'p'
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
    blank = 'b'
    using = 'u'
    reserved = 'r'
    waiting = 'w'
