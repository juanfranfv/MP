(function ($) {

    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '&#x3c;Ant',
        nextText: 'Sig&#x3e;',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Mi&eacute;rcoles', 'Jueves', 'Viernes', 'S&aacute;bado'],
        dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mi&eacute;', 'Juv', 'Vie', 'S&aacute;b'],
        dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'S&aacute;'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['es']);

    jQuery.extend(jQuery.validator.methods, {
        date: function (value, element) {
            var isChrome = window.chrome;
            // make correction for chrome
            if (isChrome) {
                var d = new Date();
                return this.optional(element) ||
                !/Invalid|NaN/.test(new Date(d.toLocaleDateString(value)));
            }
                // leave default behavior
            else {
                return this.optional(element) ||
                !/Invalid|NaN/.test(new Date(value));
            }
        }
    });

    $('input[type=date]').datepicker({
        dateFormat: 'dd/mm/yy',
        changeMonth: true,
        changeYear: true
    });

    $('input[type=date]').each(function () {
        this.type = "text";
    });


    //$("#FechaNacimiento").datepicker({
    //    dateFormat: 'dd/mm/yy',
    //    changeMonth: true,
    //    changeYear: true
    //});
    //$("#Aniversario").datepicker({
    //    dateFormat: 'dd/mm/yy',
    //    changeMonth: true,
    //    changeYear: true
    //});

    //$('input[type=date]').datepicker({ dateFormat: 'yy-mm-dd' });
})(jQuery);