//Compara la fecha hra actual, con los pedidos en reparto, para saber cuando llegan a destino
function currentTime() {
    let date = new Date(); 
    let hh = date.getHours();
    let mm = date.getMinutes();
    let ss = date.getSeconds();

    let dia = date.getDate();
    let mes = 1+ date.getMonth();
    let anno = date.getFullYear();
    let fecha = dia +"-"+ mes +"-"+ anno;

    hh = (hh < 10) ? "0" + hh : hh;
    mm = (mm < 10) ? "0" + mm : mm;
    ss = (ss < 10) ? "0" + ss : ss;

    let time = hh + ":" + mm + ":" + ss;

    document.getElementById("fecha").innerText = fecha; 
    document.getElementById("hora").innerText = time; 
    let t = setTimeout(function(){ currentTime() }, 1000);
}
currentTime();