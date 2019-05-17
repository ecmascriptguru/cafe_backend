(($) => {
    const WS_BASE_URL = `ws://${window.location.host}/ws/chat/${userId}/`,
        API_BASE_URL = `http://${window.location.host}/api/channels/`

    let chatSocket = null,
        $messagesContainer = $(".direct-chat-messages"),
        currentChannel = null
    
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
            console.info("TODO: Please implement logic here.")
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
            
                default:
                    console.log("UNKNOWN MESSAGE FOUND.")
                    console.log(data)
                    break;
            }
        },

        _socketCloseHandler = (e) => {
            console.error('Socket closed unexpectedly.')
        },

        _initSocket = () => {
            chatSocket = new WebSocket(WS_BASE_URL);
            chatSocket.onmessage = _socketMessageHandler
            chatSocket.onclose = _socketCloseHandler
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
        },

        drawChatHistory = (messages, callback) => {
            $messagesContainer.children().remove()

            for (let i = 0; i < messages.length; i ++) {
                $messagesContainer.prepend($(getHtmlMsg(messages[i])))
            }
        },

        _initEventListeners = () => {
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
            _initSocket(), _initEventListeners()
            document.querySelector('#chat-message-input').focus();

            $('li.channel').first().click()
        }

        init()    
})(jQuery)
