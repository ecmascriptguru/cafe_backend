window.$ = window.jQuery = require('jquery')

require('bootstrap')
require('admin-lte')
require('icheck')

require("../../node_modules/jquery.formset/src/jquery.formset")

import { enableLiveView } from "./utils/live";

window.EmailHunter = (() => {
    $('.carousel').carousel()
    return {
        tools: {
            enableLiveView
        }
    }
})()