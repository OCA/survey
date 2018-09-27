/* Copyright 2018 ACSONE SA/NV
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).*/

$(document).ready(function () {
    'use strict';
    $(".rate > label").click(function () {
        var label_items = $( this ).parent().find("label");
        var value = label_items.length - $( this ).index();
        label_items.removeClass("checked");
        label_items.slice($( this ).index()).addClass("checked");
        $( this ).parent().find("input").val(value);
    });
});
