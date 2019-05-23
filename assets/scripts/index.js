window.$ = window.jQuery = require('jquery')

require('bootstrap')
require('admin-lte')
require('icheck')

require("../../node_modules/jquery.formset/src/jquery.formset")
window.Amplitude = require('../../node_modules/amplitudejs/dist/amplitude')

import { enableLiveView } from "./utils/live";
import { initSocket } from "./modules/socket";

window.CafeAdmin = (() => {
    initSocket()
    return {
        name: 'Cafe Backend Administration App'
    }
})()