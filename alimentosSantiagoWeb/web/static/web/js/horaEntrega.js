
function deliveryDate(fecha){
    //var date = new Date(fecha); 
    var fechapedido = fecha
    return fecha;
}

var fechaPasada = deliveryDate(fecha);

//Compara la fecha hra actual, con los pedidos en reparto, para saber cuando llegan a destino
function currentTime() {

    //fecha estatica pedido
    var annoPedido = '2022'
    var mesPedido = '5'     //mes va de 0 a 11. Se le debe RESTAR 1 en PEDIDO
    var diaPedido = '6'
    var horaPedido = '11'
    var minPedido = '17'

    //var pedido = new Date(annoPedido, mesPedido, diaPedido, horaPedido, minPedido)
    var pedido = fechaPasada
    document.getElementById("fechaPedido").innerText = pedido; 

    //fecha hora actual
    let date = new Date(); 
    let hh = date.getHours();
    let mm = date.getMinutes();
    let ss = date.getSeconds();

    let dia = date.getDate();
    let mes = 1+ date.getMonth();       //mes va de 0 a 11. Se le debe SUMAR 1 en ACTUAL
    let anno = date.getFullYear();
    let fecha = dia +"-"+ mes +"-"+ anno;

    hh = (hh < 10) ? "0" + hh : hh;
    mm = (mm < 10) ? "0" + mm : mm;
    ss = (ss < 10) ? "0" + ss : ss;

    let time = hh + ":" + mm + ":" + ss;

    document.getElementById("fechaActual").innerText = date; 
    document.getElementById("fecha").innerText = fecha; 
    document.getElementById("hora").innerText = time; 

    //if comparativo
    /*if (pedido <= date){
        document.getElementById("pedidoEntregado").innerText = 'Si';   
    } else{
        document.getElementById("pedidoEntregado").innerText = 'No'; 
    }*/

    
    let t = setTimeout(function(){ currentTime() }, 1000);
}
currentTime();