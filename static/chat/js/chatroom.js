(($) => {
    var chatSocket = new WebSocket(
        `ws://${window.location.host}/ws/chat/${userId}/`);
    
    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'].message;
        document.querySelector('#chat-log').value += (message + '\n');
    };
    
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
    
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    
    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'group': `channel_2`,
        }));
    
        messageInputDom.value = '';
    };
})(jQuery)
