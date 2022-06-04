//tiene bug, ya que no deberia poder pedir para hoy en una hora que ya pasó
//pero para los otros dias que agarre el mintime 0700
$(function () {
    //fecha en carrito
    $("#id_fecha_programada").datetimepicker({
        inline:true,
        dayOfWeekStart: '1',    //empieza el lunes
        startDate:'{{ carrito.fecha_programada }}',
        minDate:'0',            //el minimo es hoy
        maxDate:'+1970/02/01',  //el maximo es en un mes
        minTime: '07:00',
        maxTime: '21:00',
        step:10,
        format: 'm/d/Y H:i'  
    });
    //fecha en crud producto
    $("#id_fecha_publicacion").datetimepicker({
        inline:true,
        dayOfWeekStart: '1',    //empieza el lunes
        startDate:'0',
        defaultDate:'+1970/01/01',
        defaultTime:0,
        minDate:0,           
        maxDate:'+1970/01/07',
        step:10,
        format: 'm/d/Y H:i',
    });
});

$(document).ready(function () {  
    jQuery.datetimepicker.setLocale('es');  
});  