(function($) {
    const EVENT_TPYE = {
            just_once: 'o',
            every_week: 'w',
            every_day: 'd'
        },
        $weekdayContainer = $('.weekday-checkbox')//.closest('div.form-row')
        
    $(document).on('change', '#id_repeat', function(event) {
        $weekdayContainer.prop('disabled', ($(this).val() != EVENT_TPYE.every_week))
    });
})(django.jQuery);