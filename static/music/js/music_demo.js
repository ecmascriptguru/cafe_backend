const MusicDemo = (($) => {
    const API_BASE_URL = '/api/music/',
        $keywordInput = $('#music-search-keyword'),
        $searchSubmitButton = $('#music-search-submit'),
        $searchResultContainer = $('.music-search-result-container'),
        apiPaths = {
            search: 'search'
        }

    /**
     * Default function to send ajax request to Music API server
     * @param {JSON} data 
     * @param {Function} success 
     * @param {Function} failure 
     */
    const sendRequest = (path, data, success, failure) => {
        $.ajax({
            url: `${API_BASE_URL}${path}`,
            data,
            success: (res) => { success(res) },
            failure: (e) => {
                if (failure && typeof failure === 'function') {
                    failure(e)
                } else {
                    console.error("Failed!!!")
                }
            }
        })
    }

    /**
     * 
     * @param {String} keyword 
     * @param {Function} success 
     * @param {Function} failure 
     */
    const searchMusic = (keyword, success, failure) => {
        sendRequest(apiPaths.search, { keyword }, (res) => {
            success(res)
        }, failure)
    }

    const renderSearchResults = (musics) => {
        $searchResultContainer.children().remove()
        for (let idx in musics) {
            let music = musics[idx]
            $searchResultContainer.append($(`<div class='nav-item music row form-group' data-external-id=${music.songid}>
                <span class='music-author col-xs-3'>${music.artistname}</span>
                <span class='music-title col-xs-8'>${music.songname}</span>
                <span class='music-action col-xs-1 pull-right'>
                    <button class='btn btn-xs'>Play</button>
                </span>
            </div>`))
        }
    }

    const _init = () => {
        $(document)
        .on('change', '#music-search-keyword', (e) => {
            if (e.target.value == '') {
                $searchSubmitButton.prop('disabled', true)
            } else {
                $searchSubmitButton.prop('disabled', false)
            }
        })
        .on('keyup', '#music-search-keyword', (e) => {
            if (e.keyCode === 13 && $keywordInput.val() != '') {
                $searchSubmitButton.click()
            }
        })
        .on('click', '#music-search-submit', (e) => {
            searchMusic($keywordInput.val(), (musics) => {
                renderSearchResults(musics)
            })
        })
    }

    _init()

    return {
        name: "Music Demo Player"
    }
})(jQuery)