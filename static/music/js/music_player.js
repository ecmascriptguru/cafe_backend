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

        document.getElementById('song-played-progress').addEventListener('click', function( e ){
            var offset = this.getBoundingClientRect();
            var x = e.pageX - offset.left;
        
            Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
        });
    }

    init()

    return {
        name: "WAT ARE YOU DOINHG NOW?",
        init: () => { console.error("Your browser will behavior oddly soon") },
        getPlayer: () => { return playerObject }
    }
})(jQuery)
