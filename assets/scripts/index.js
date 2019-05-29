window.$ = window.jQuery = require('jquery')

require('bootstrap')
require("../../node_modules/admin-lte/bower_components/bootstrap-datepicker/dist/js/bootstrap-datepicker")
require("../../node_modules/admin-lte/plugins/timepicker/bootstrap-timepicker")
require('admin-lte')
require('icheck')

require("../../node_modules/jquery.formset/src/jquery.formset")
window.Amplitude = require('../../node_modules/amplitudejs/dist/amplitude')

import { enableLiveView } from "./utils/live";
import { initSocket } from "./modules/socket";

window.CafeAdmin = (() => {
    $(document).ready(() => {
        $(".date-picker").datepicker("YYYY-MM-DD")
        $(".time-picker").timepicker({showMeridian: false})
    })
    initSocket()
    return {
        name: 'Cafe Backend Administration App'
    }
})()