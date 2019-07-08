$(document).ready(() => {
    let selectedItems = {}
    const ORDER_ITEM_STATES = {delivered: 'e', canceled: 'c'},
        $modalSelectedItemsTable = $('table#selected-order-items-container tbody'),
        $deliveredButton = $('button#delivered-confirm'),
        $canceledButton = $('button#canceled-confirm'),
        token = $('input:hidden[name=csrfmiddlewaretoken]').val(),
        API_BASE_URL = `/api/`,
        send_request = (url, data, method, success, failure) => {
            if (['post', 'put', 'patch'].indexOf(method.toLowerCase()) !== -1) {
                data['csrfmiddlewaretoken'] = token
            }

            $.ajax({
                url, method, data: JSON.stringify(data),
                contentType: 'application/json',
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
        addItems = (items_data, success, failure) => {
            items = []
            for (let key in items_data) {
                items.push(items_data[key])
            }
            send_request(`${API_BASE_URL}orders/${window.orderId}/add_items/`, {"items": items}, 'post', success, failure)
        },
        updateItem = (id, amount, success, failure) => {
            send_request(`${API_BASE_URL}items/${id}/set_amount/`, { amount }, 'post', success, failure)
        },
        markItemsDelivered = (item_ids, success, failure) => {
            markItems(item_ids, ORDER_ITEM_STATES.delivered, success, failure)
        },
        markItemscanceled = (item_ids, success, failure) => {
            markItems(item_ids, ORDER_ITEM_STATES.canceled, success, failure)
        },
        updateModalStatisticsData = () => {
            let sum = 0,
                free = 0,
                billing = 0
            
            for (let key in selectedItems) {
                let item = selectedItems[key]
                sum += item.price * item.amount
                free += (item.free ? item.price * item.amount : 0)
            }
            billing = sum - free
            $('.additional-sum').text(sum)
            $('.additional-free').text(free)
            $('.additional-billing').text(billing)
        },
        updateCheckoutForm = () => {
            const $form = $('form#order-checkout-form'),
                $deposit = $form.find('input[name=deposit]'),
                $sum = $form.find('input[name=total]'),
                $additional_money = $form.find('input[name=additional_money]'),
                $wipe_zero = $form.find('input[name=wipe_zero]'),
                $income = $form.find('input[name=earning]'),
                $change = $form.find('input[name=change]')
            
            let data = {
                    deposit: parseFloat($deposit.val()),
                    sum: parseFloat($sum.val()),
                    additional_money: parseFloat($additional_money.val() || 0),
                    wipe_zero: parseFloat($wipe_zero.val()),
                },
                income = data.sum - data.wipe_zero,
                change = data.deposit + data.additional_money - income

            $income.val(income)
            $change.val(change)
        }

        $.ajaxSetup({ 
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            } 
        });

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
    .on('click', 'button#send-additional-items-ok', function() {
        addItems(selectedItems, (res) => {
            window.location.reload()
        }, () => {})
        console.log(selectedItems)
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
        $self.closest('div.modal').modal('hide')
    })
    .on('click', 'div.order-item-card', function() {
        let $self = $(this)

        $self.toggleClass('active')
        if ($self.hasClass('active')) {
            let item = {
                id: $self.data('dish-id'),
                name: $self.data('dish-name'),
                price: parseFloat($self.data('dish-price')),
                amount: 1,
                free: false
            }
            selectedItems[`dish_${item.id}`] = item
            $modalSelectedItemsTable.append(
                $(`<tr data-dish-id="${item.id}" class="modal-selected-dish-record">
                    <td class="item-dish-name">${item.name}</td>
                    <td>&yen; <span class="item-dish-price">${item.price}</span></td>
                    <td><input type="number" class="form-control item-amount" value="1" /></td>
                    <td><input type="checkbox" class="item-free" /></td>
                    <td>&yen; <span class="item-sub-total">${item.price}</span></td>
                </tr>`)
            )
        } else {
            let dishId = $self.data('dish-id')
            if (selectedItems[`dish_${dishId}`]) {
                delete selectedItems[`dish_${dishId}`]
            }
            $modalSelectedItemsTable.find(`tr.modal-selected-dish-record[data-dish-id=${dishId}]`).remove()
        }

        updateModalStatisticsData()
    })
    .on('change', 'tr.modal-selected-dish-record input.item-amount', function() {
        let $self = $(this),    
            id = $self.closest('tr').data('dish-id')
        const price = selectedItems[`dish_${id}`].price
        $self.closest('tr').find('span.item-sub-total').text(price * $self.val())
        selectedItems[`dish_${id}`]['amount'] = parseInt($self.val())
        updateModalStatisticsData()
    })
    .on('change', 'tr.modal-selected-dish-record input.item-free', function() {
        let $self = $(this),    
            id = $self.closest('tr').data('dish-id')
        const { price, amount } = selectedItems[`dish_${id}`]
        $self.closest('tr').find('span.item-sub-total').text(price * amount)
        selectedItems[`dish_${id}`]['free'] = $self.prop('checked')
        updateModalStatisticsData()
    })
    .on('change', 'form#order-checkout-form input[name=additional_money], form#order-checkout-form input[name=wipe_zero]', function() {
        updateCheckoutForm()
    })
    .on('click', 'button#checkout-order', function() {
        $form = $(this).closest('div.modal').find('form')
        $form.submit()
    })
    .on('change', 'input.dish-amount-input', function() {
        let $self = $(this),
            id = $self.closest('tr').data('item-id'),
            value = $self.val(),
            is_free = JSON.parse($self.data('item-free').toLowerCase())
        updateItem(id, value, (res) => {
            window.location.reload()
        })
    })
})