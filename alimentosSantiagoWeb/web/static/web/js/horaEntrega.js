//Compara la fecha hra actual, con los pedidos en reparto, para saber cuando llegan a destino
function currentTime() {
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

    let hora = hh + ":" + mm + ":" + ss;

    document.getElementById("fecha").innerText = fecha; 
    document.getElementById("hora").innerText = hora; 

    document.getElementById("fechaPedido").innerText = pedidoFecha; 
    document.getElementById("horaPedido").innerText = pedidoHora; 

    //if comparativo
    if (pedidoFecha <= fecha){
        if (pedidoHora <= hora){
            document.getElementById("pedidoEntregado").innerText = 'Si';   
            window.location.href = '/pedido-entregado/'+id+'/';
        } else{
            document.getElementById("pedidoEntregado").innerText = 'No'; 
        }
    }
    let t = setTimeout(function(){ currentTime() }, 1000);
}
currentTime();