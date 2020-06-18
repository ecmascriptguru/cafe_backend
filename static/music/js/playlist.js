(function() {
    const BASE_URL = '/api/playlist/',
        token = $('input:hidden[name=csrfmiddlewaretoken]').val(),
        processPlaylistItem = (pk, success, failure) => {
            $.ajax({
                url: `${BASE_URL}${pk}/spotify_process`,
                method: 'get',
                success: (res) => {
                    if (typeof success === 'function') {
                        success(res)
                    } else {
                        console.log(res)
                    }
                },
                error: () => {
                    if (typeof failure === 'function') {
                        failure()
                    } else {
                        console.error("Failed to process spotify music")
                    }
                }
            })
        },
        clearPlaylist = (success, failure) => {
            $.ajax({
                url: `${BASE_URL}clear/`,
                method: 'post',
                data: {csrfmiddlewaretoken: token},
                success: (res) => {
                    if (typeof success === 'function') {
                        success(res)
                    } else {
                        console.log(res)
                    }
                },
                error: () => {
                    if (typeof failure === 'function') {
                        failure()
                    } else {
                        console.error("Failed to process spotify music")
                    }
                }
            })
        }
    $(document)
    .on('click', 'button.playlist-process', function() {
        let pk = $(this).data('id'),
            url = $(this).data('href')
        
        processPlaylistItem(pk, (res) => {
            console.log(res)
            let win = window.open(url, '_blank')
            win.focus()
            window.location.reload()
        })
    })
    .on('click', '#music-clear-button', function() {
        clearPlaylist((res) => {
            window.location.reload()
        })
    })
})()