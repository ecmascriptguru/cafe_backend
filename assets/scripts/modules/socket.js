export const initSocket = () => {
    const WS_BASE_URL = `ws://${window.location.host}/ws/chat/${userId}/`,
        API_BASE_URL = `http://${window.location.host}/api/channels/`,
        MONITOR_BASE_URL = `ws://${window.location.host}/ws/monitor/${userId}/`

    let chatSocket = null,
        $messagesContainer = $(".direct-chat-messages"),
        currentChannel = null,
        socket_reset_timer = null,
        ringTone = null,
        orderAlert = null
    
    const showNotificationOnChannel = (channelID) => {
            if ($(`li.channel[data-channel-id=${channelID}]`).length == 0) {
                return false
            } else {
                let $channelContainer = $(`li.channel[data-channel-id=${channelID}]`),
                    $badge = $channelContainer.find('span.badge')
                if ($badge.length == 0) {
                    $badge = $(`<span class="badge">1</span>`).appendTo($channelContainer)
                } else {
                    let originCount = parseInt($badge.text() || 0)
                    originCount++
                    $badge.text(originCount)
                }
            }
        },

        _handleChatMessage = (data) => {
            let message = data['message'];
            
            if (message.channel_id == currentChannel) {
                $messagesContainer.append(getHtmlMsg(message))
            } else {
                // Show notification
                showNotificationOnChannel(message.channel_id)
            }
        },

        _handleEventNotification = (data) => {
            const $orderNotificationContainer = $('')
            console.info("TODO: Please implement logic here.")
        },

        _handleOrderNotification = (data) => {
            const $notificationContainer = $(".orders-menu"),
                $count = $(".new-order-count")

            if (!orderAlert) {
                orderAlert = new Audio(document.querySelector('#order-alert').src)
            }

            orderAlert.play()
            $notificationContainer.find("ul li.header").hide()
            if ($notificationContainer.find(`li.order-notification`).length == 0) {
                let notification_count = parseInt($count.text() || "0") + 1
                $count.text(notification_count)
                $notificationContainer.find("ul.menu.order-notification-list").append($(`
                    <li class='order-notification'">
                        <a href="#">
                            <div class="pull-left">
                                <span></span>
                            </div>
                            <p>${window.new_order_notification_message}</p>
                        </a>
                    </li>`))
            }
        },

        _handleTableRingNotification = (table) => {
            const $notificationContainer = $(".notifications-menu"),
                $count = $(".notification-count")

            if (!ringTone) {
                ringTone = new Audio(document.querySelector('#table-ring-tone').src)
            }

            ringTone.play()
            $notificationContainer.find("ul li.header").hide()
            if ($notificationContainer.find(`li.ring-notification[data-table-user-id=${table.user_id}]`).length == 0) {
                let notification_count = parseInt($count.text() || "0") + 1
                $count.text(notification_count)
                $notificationContainer.find("ul.menu").append($(`
                    <li data-table-user-id="${table.user_id}" class="ring-notification">
                        <a href="#">
                            <i class="fa fa-bell-o"></i>${table.name} is calling...
                            <button class="btn btn-xs pull-right mark-notification-as-read"><i class="fa fa-check"></i></button>
                        </a>
                    </li>`))
            }
        },

        _socketMessageHandler = (e) => {
            let data = JSON.parse(e.data)

            switch (data.type) {
                case 'chat_message':
                    _handleChatMessage(data)
                    break;

                case 'notification_event':
                    _handleEventNotification(data)
                    break;
            
                case 'notification_order':
                    if (data.created) {
                        console.info("Order Created")
                        console.log(data.order)
                    }
                    break;
            
                case 'notification_order_item':
                    // if (data.created) {
                        _handleOrderNotification(data)
                    // }
                    break;
            
                case 'ring':
                    _handleTableRingNotification(data.table)
                    break;

                default:
                    console.log("UNKNOWN MESSAGE FOUND.")
                    console.log(data)
                    break;
            }
        },

        _socketCloseHandler = (e) => {
            console.error('Socket closed unexpectedly. Retrying to connect...')
            socket_reset_timer = window.setInterval(
                () => {
                    try {
                        _initSocket();
                        window.clearInterval(socket_reset_timer)
                    } catch(e) {
                        console.error(e)
                    }
                },
            1000)
            
        },

        _initSocket = () => {
            chatSocket = new WebSocket(WS_BASE_URL);
            chatSocket.onmessage = _socketMessageHandler
            chatSocket.onclose = _socketCloseHandler

            /**
             * Testing monitor socket
             */
            chatSocket = new WebSocket(MONITOR_BASE_URL);
        },

        getChannel = (channelID, callback) => {
            $.ajax({
                url: `${API_BASE_URL}${channelID}`,
                method: 'get',
                contentType: 'application/json',
                success: (res) => {
                    (callback && typeof callback === 'function') && callback(res)
                }
            })
        },

        getHtmlMsg = (msg) => {
            const isMine = (userId == msg.poster)

            if (msg.content != '') {
                return `<div class="direct-chat-msg${isMine ? ' right' : ''}">
                    <div class="direct-chat-info clearfix">
                        <span class="direct-chat-name ${isMine ? 'pull-right' : 'pull-left'}">${msg.poster_name}</span>
                        <span class="direct-chat-timestamp ${isMine ? 'pull-left' : 'pull-right'}">${(new Date(msg.created)).toLocaleString()}</span>
                    </div>
                    <!-- /.direct-chat-info -->
                    <div class="direct-chat-text">
                    ${msg.content}
                    </div>
                    <!-- /.direct-chat-text -->
                </div>`
            } else {
                return ''
            }
            
        },

        drawChatHistory = (messages, callback) => {
            $messagesContainer.children().remove()

            for (let i = 0; i < messages.length; i ++) {
                $messagesContainer.prepend($(getHtmlMsg(messages[i])))
            }
        },

        _initChatRoomEventListeners = () => {
            $(document)
            .on('keyup', '#chat-message-input', function(e) {
                if (e.keyCode === 13) {  // enter, return
                    document.querySelector('#chat-message-submit').click();
                }
            })
            .on('click', '#chat-message-submit', function(e) {
                var messageInputDom = document.querySelector('#chat-message-input');
                var message = messageInputDom.value;

                if (!message) return false

                chatSocket.send(JSON.stringify({
                    message: message,
                    to: currentChannel
                }));
            
                messageInputDom.value = '';
            })
            .on('click', 'li.channel', function(e) {
                currentChannel = $(this).data('channel-id')
                $('li.channel.active').removeClass('active')
                getChannel(currentChannel, (res) => {
                    $(this).addClass('active').find('span.badge').remove()
                    $(".channel-name").text(res.name)
                    if (res.message_set) {
                        drawChatHistory(res.message_set)
                    }
                })
            })
            
        },

        init = () => {
            _initSocket()

            $(document)
            .on('keyup', '#chat-message-input', function(e) {
                if (e.keyCode === 13) {  // enter, return
                    document.querySelector('#chat-message-submit').click();
                }
            })
            .on('click', '#chat-message-submit', function(e) {
                var messageInputDom = document.querySelector('#chat-message-input');
                var message = messageInputDom.value;

                if (!message) return false

                chatSocket.send(JSON.stringify({
                    message: message,
                    to: currentChannel
                }));
            
                messageInputDom.value = '';
            })
            .on('click', 'li.channel', function(e) {
                currentChannel = $(this).data('channel-id')
                $('li.channel.active').removeClass('active')
                getChannel(currentChannel, (res) => {
                    $(this).addClass('active').find('span.badge').remove()
                    $(".channel-name").text(res.name)
                    if (res.message_set) {
                        drawChatHistory(res.message_set)
                    }
                })
            })
            .on("click", "button.mark-notification-as-read", function() {
                let $self = $(this),
                    $container = $self.closest('.notifications-menu'),
                    $count = $(".notification-count")
                let current_notification_count = JSON.parse($count.text()) - 1

                $self.closest('li').remove()
                if (current_notification_count == 0) {
                    $count.text('')
                    $container.find('li.header').show()
                } else {
                    $count.text(current_notification_count)
                }
            })
            if (document.querySelector('#chat-message-input')) {
                _initChatRoomEventListeners()

                document.querySelector('#chat-message-input').focus();
                $('li.channel').first().click()
            }

            if ($('li.channel').length > 0) {
                $('li.channel').first().click()
            }
        }
    init()
}