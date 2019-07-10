const MusicPlayer = (($) => {
    const API_BASE_URL = '/api/playlist/',
        $coverArtImage = $('#amplitude-album-art'),
        $title = $('.amplitude-now-playing-title'),
        $artist = $('.amplitude-now-playing-artist'),
        $playlist = $('#player-playlist')

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
            let songs = musics.map(item => {
                return {
                    name: item.title,
                    cover_art_url: item.picture,
                    url: item.url,
                    artist: item.author,
                    external_id: item.external_id,
                    pk: item.pk
                }
            })

            let indice = []
            for (let idx in musics) {
                indice.push(idx)
            }

            let settings = {
                    songs: songs,
                    playlists: {
                        'temp': {
                            songs: songs,
                            title: "all"
                        }
                    },
                    debug: true,
                    callbacks: {
                        song_change: function() {
                            let activeMeta = Amplitude.getActivePlaylistMetadata(),
                                songIndex = activeMeta.active_index,
                                songObj = activeMeta.songs[songIndex]
                            
                            $coverArtImage[0].src = songObj.cover_art_url
                            $title.text(songObj.name)
                            $artist.text(songObj.artist)
                            $playlist.children().removeClass('active')
                            $playlist.children().eq(songIndex).addClass('active')

                            sendRequest(`${songObj.pk}/archive/`, 'get', {}, (res) => {
                                if (res.status) {
                                    // Amplitude.removeSong(songIndex)
                                    $playlist.find(`div.playlist-song[data-external-id=${songObj.external_id}]`).remove()
                                }
                            })
                        }
                    }
                }
            const $playerPlaylist = $('#player-playlist')

            $playerPlaylist.children().remove()
            for (let idx in settings.songs) {
                let item = settings.songs[idx]
                $playerPlaylist.append($(`<div class="playlist-song" data-external-id="${item.external_id}" data-index="${idx} id="song-${idx}">
                    <div class="playlist-song-album-art">
                        <img src="${item.cover_art_url}">
                    </div>
                    <div class="playlist-song-information">
                        Song: ${item.name}<br>
                        Artist: ${item.artist}<br>
                        Album: Cafe Backend
                    </div>
                </div>`))
            }
            playerObject = Amplitude.init(settings)

            if (songs.length > 0) {
                $coverArtImage[0].src = songs[0].cover_art_url
                $title.text(songs[0].name)
                $artist.text(songs[0].artist)
                $playlist.children().eq(0).addClass('active')
            }

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
