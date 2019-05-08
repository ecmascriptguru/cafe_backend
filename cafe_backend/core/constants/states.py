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
    draft = DEFAULT_STATE.draft
    default = DEFAULT_STATE.default
    in_progress = DEFAULT_STATE.in_progress
    canceled = DEFAULT_STATE.canceled
    delivered = DEFAULT_STATE.delivered
    archieved = DEFAULT_STATE.archived
