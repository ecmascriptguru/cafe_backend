const MusicPlayer = (($) => {
    const API_BASE_URL = '/api/playlist/'
    let playerObject = null

    /**
     * Basic function to http request to API server
     * @param {String} path 
     * @param {String} method 
     * @param {Json} data 
     * @param {Function} success 
     * @param {Function} failure 
     */
    const sendRequest = (path, method, data, success, failure) => {
        $.ajax({
            url: `${API_BASE_URL}${path}`,
            contentType: 'application/json',
            data,
            type: method,
            success,
            error: failure
        })
    }

    /**
     * Function to grab music playlist
     * @param {Function} success 
     * @param {Function} failure 
     */
    const getPlaylist = (success, failure) => {
        sendRequest('', 'get', {}, success, failure)
    }

    const init = () => {
        // grabbing musics
        getPlaylist((musics) => {
            playerObject = Amplitude.init({
                songs: musics.map(item => {
                        return {
                            name: item.title,
                            cover_art_url: item.picture,
                            url: item.url,
                            artist: item.customer,
                            album: ''
                        }
                    })
                }
            )
        })
    }

    init()

    return {
        name: "WHAT ARE YOU DOING NOW?",
        init: () => { console.error("Your browser will behavior oddly soon") }
    }
})(jQuery)
