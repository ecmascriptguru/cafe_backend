$(document).ready(() => {
    const ORDER_ITEM_STATES = {delivered: 'e', canceled: 'c'},
        $deliveredButton = $('button#delivered-confirm'),
        $canceledButton = $('button#canceled-confirm'),
        token = $('input:hidden[name=csrfmiddlewaretoken]').val(),
        API_BASE_URL = `/api/`,
        send_request = (url, data, method, success, failure) => {
            if (['post', 'put', 'patch'].indexOf(method.toLowerCase()) !== -1) {
                data['csrfmiddlewaretoken'] = token
            }

            $.ajax({
                url, method, data,
                success: (res) => {
                    if (res.status) {
                        success(res)
                    } else {
                        if (typeof failure === 'function') {
                            failure(res)
                        } else {
                            console.log(res)
                        }
                    }
                },
                error: () => { failure() }
            })
        },
        markItems = (item_ids, state, success, failure) => {
            data = {
                item_ids, state
            }
            send_request(`${API_BASE_URL}orders/${window.orderId}/update_items/`, data, 'post', success, failure)
        },
        markItemsDelivered = (item_ids, success, failure) => {
            markItems(item_ids, ORDER_ITEM_STATES.delivered, success, failure)
        },
        markItemscanceled = (item_ids, success, failure) => {
            markItems(item_ids, ORDER_ITEM_STATES.canceled, success, failure)
        }

    $(document)
    .on('change', 'table#order-items-table tr input:checkbox', function() {
        let valid = !$('table#order-items-table tr input:checkbox:checked').length > 0
        $deliveredButton.prop('disabled', valid)
        $canceledButton.prop('disabled', valid)
    })
    .on('click', 'table#order-items-table tr', function() {
        let cur = $(this).find('input:checkbox').prop('checked')
        if (event.target.tagName !== 'INPUT') {
            $(this).find('input:checkbox').prop('checked', !cur).change()
        }
    })
    .on('click', 'button.update-items-ok', function() {
        let state = ORDER_ITEM_STATES[$(this).data('value')],
            ids = $('table#order-items-table tr input:checkbox:checked').map((idx, el) => $(el).val()).get()
        markItems(ids, state, (res) => {
            window.location.reload()
        }, () => {alert('Someting went wrong!')})
    })
    .on('click', 'button#print-order', function() {
        const $self = $(this)
        // To do
        $self.prop('disabled', true)
        send_request(`${API_BASE_URL}orders/${window.orderId}/print/`, {}, 'get', (res) => {
            console.log(res)
        }, () => {})
        window.setTimeout(() => {
            $self.prop('disabled', false)
        }, 10000)
    })
})