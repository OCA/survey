/* Copyright 2016 ONESTEiN BV (<http://www.onestein.eu>)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

(function ($) {
    'use strict';
    //Remove default radio click behaviour
    $('.survey_restricted_radio').click(function(e) {
        e.preventDefault();
    });
    
    //Remove default radio mouseup behaviour
    $('.survey_restricted_radio').mouseup(function(e) {
        e.preventDefault();
    });
    
    //Add custom radio button behaviour
    $('.survey_restricted_radio').mousedown(function(e) {
        if($('input[name="' + $(this).attr('name') + '"]').is(':checked')) {
            var val = $('input[name="' + $(this).attr('name') + '"]:checked').val();
            $('input[value="' + val + '"]').not(this).removeAttr('disabled');
        }
        if(!$(this).is(':checked')) {
            $(this).attr('checked', 'checked');
            $('input[value="' + $(this).val() + '"]').not(this).attr('disabled', 'disabled');
        } else {
            $(this).removeAttr('checked');
            $('input[value="' + $(this).val() + '"]').not(this).removeAttr('disabled');
        }
    });
})(jQuery);
