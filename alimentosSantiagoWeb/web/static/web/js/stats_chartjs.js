/*MONTO DE VENTAS Envio-Retiro*/
let myChart_envio = document.getElementById('barChart_envio').getContext('2d');
let montEnvioChart = new Chart(myChart_envio, {
    type:'pie', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        'Envio Domicilio', 'Retiro en Local'
        ],
        datasets:[{
            label:'Monto Total Ventas',
            data:[
            total_envio,
            total_retiro
            ],
            backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 205, 86)'],
            hoverOffset: 10
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*CANTIDAD DE PRODUCTOS Envio-Retiro*/
let myChart_envioCant = document.getElementById('barChart_envioCant').getContext('2d');
let montEnvioCantChart = new Chart(myChart_envioCant, {
    type:'pie', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        'Envio Domicilio', 'Retiro en Local'
        ],
        datasets:[{
            label:'Cantidad Productos Vendidos',
            data:[
                cant_envio,
                cant_retiro
            ],
            backgroundColor: ['rgb(63, 224, 195)', 'rgb(230, 50, 188)'],
            hoverOffset: 10
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*MONTO DE VENTAS Programado-No programado*/
let myChart_prog = document.getElementById('barChart_prog').getContext('2d');
let montProgChart = new Chart(myChart_prog, {
    type:'pie', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        'Pedido Programado', 'Pedido No Programado'
        ],
        datasets:[{
            label:'Monto Total Ventas',
            data:[
            total_prog,
            total_no_prog
            ],
            backgroundColor: ['rgba(245, 66, 66, 0.7)', 'rgba(245, 212, 66, 0.7)'],
            hoverOffset: 10
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*CANTIDAD DE PRODUCTOS Programado-No programado*/
let myChart_progCant = document.getElementById('barChart_progCant').getContext('2d');
let montProgCantChart = new Chart(myChart_progCant, {
    type:'pie', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
            'Pedido Programado', 'Pedido No Programado'
        ],
        datasets:[{
            label:'Cantidad Productos Vendidos',
            data:[
                cant_prog,
                cant_no_prog
            ],
            backgroundColor: ['rgb(63, 224, 195)', 'rgb(230, 50, 188)'],
            hoverOffset: 10
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*MONTO DE VENTAS ULTIMOS 7 DIAS*/
let myChart_7 = document.getElementById('barChart_7').getContext('2d');
let mont7Chart = new Chart(myChart_7, {
    type:'line', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        fechas7dias[0].replace(/[^0-9--]/g, ''),
        fechas7dias[1].replace(/[^0-9--]/g, ''),
        fechas7dias[2].replace(/[^0-9--]/g, ''),
        fechas7dias[3].replace(/[^0-9--]/g, ''),
        fechas7dias[4].replace(/[^0-9--]/g, ''),
        'Ayer '+ fechas7dias[5].replace(/[^0-9--]/g, ''),
        'Hoy '+ fechas7dias[6].replace(/[^0-9--]/g, '')
        ],
        datasets:[{
            label:'Monto Total Ventas',
            data:[
            ventas7dias[0].replace(/[^0-9]/g, ''),
            ventas7dias[1].replace(/[^0-9]/g, ''),
            ventas7dias[2].replace(/[^0-9]/g, ''),
            ventas7dias[3].replace(/[^0-9]/g, ''),
            ventas7dias[4].replace(/[^0-9]/g, ''),
            ventas7dias[5].replace(/[^0-9]/g, ''),
            ventas7dias[6].replace(/[^0-9]/g, '')
            ],
            pointRadius: 5,
            pointHoverRadius: 10,
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgba(245, 66, 66)'
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*MONTO DE VENTAS ULTIMOS 6 MESES*/
let myChart_6 = document.getElementById('barChart_6').getContext('2d');
let mont6Chart = new Chart(myChart_6, {
    type:'line', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        fechas6meses[0].replace(/[^0-9--]/g, ''),
        fechas6meses[1].replace(/[^0-9--]/g, ''),
        fechas6meses[2].replace(/[^0-9--]/g, ''),
        fechas6meses[3].replace(/[^0-9--]/g, ''),
        fechas6meses[4].replace(/[^0-9--]/g, ''),
        fechas6meses[5].replace(/[^0-9--]/g, '')
        ],
        datasets:[{
            label:'Monto Total Ventas',
            data:[
            ventas6meses[0].replace(/[^0-9]/g, ''),
            ventas6meses[1].replace(/[^0-9]/g, ''),
            ventas6meses[2].replace(/[^0-9]/g, ''),
            ventas6meses[3].replace(/[^0-9]/g, ''),
            ventas6meses[4].replace(/[^0-9]/g, ''),
            ventas6meses[5].replace(/[^0-9]/g, '')
            ],
            pointRadius: 5,
            pointHoverRadius: 10,
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgba(245, 66, 66)'
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

/*MONTO DE VENTAS ULTIMOS 30 DIAS*/
let myChart_30 = document.getElementById('barChart_30').getContext('2d');
let mont30Chart = new Chart(myChart_30, {
    type:'line', //bar,horizontalBar,pie,line,doughnut,radar,polarArea
    data:{
        labels:[
        fechas30dias[0].replace(/[^0-9--]/g, ''),
        fechas30dias[1].replace(/[^0-9--]/g, ''),
        fechas30dias[2].replace(/[^0-9--]/g, ''),
        fechas30dias[3].replace(/[^0-9--]/g, ''),
        fechas30dias[4].replace(/[^0-9--]/g, ''),
        fechas30dias[5].replace(/[^0-9--]/g, ''),
        fechas30dias[6].replace(/[^0-9--]/g, ''),
        fechas30dias[7].replace(/[^0-9--]/g, ''),
        fechas30dias[8].replace(/[^0-9--]/g, ''),
        fechas30dias[9].replace(/[^0-9--]/g, ''),
        fechas30dias[10].replace(/[^0-9--]/g, ''),
        fechas30dias[11].replace(/[^0-9--]/g, ''),
        fechas30dias[12].replace(/[^0-9--]/g, ''),
        fechas30dias[13].replace(/[^0-9--]/g, ''),
        fechas30dias[14].replace(/[^0-9--]/g, ''),
        fechas30dias[15].replace(/[^0-9--]/g, ''),
        fechas30dias[16].replace(/[^0-9--]/g, ''),
        fechas30dias[17].replace(/[^0-9--]/g, ''),
        fechas30dias[18].replace(/[^0-9--]/g, ''),
        fechas30dias[19].replace(/[^0-9--]/g, ''),
        fechas30dias[20].replace(/[^0-9--]/g, ''),
        fechas30dias[21].replace(/[^0-9--]/g, ''),
        fechas30dias[22].replace(/[^0-9--]/g, ''),
        fechas30dias[23].replace(/[^0-9--]/g, ''),
        fechas30dias[24].replace(/[^0-9--]/g, ''),
        fechas30dias[25].replace(/[^0-9--]/g, ''),
        fechas30dias[26].replace(/[^0-9--]/g, ''),
        fechas30dias[27].replace(/[^0-9--]/g, ''),
        fechas30dias[28].replace(/[^0-9--]/g, ''),
        fechas30dias[29].replace(/[^0-9--]/g, '')
        ],
        datasets:[{
            label:'Monto Total Ventas',
            data:[
            ventas30dias[0].replace(/[^0-9]/g, ''),
            ventas30dias[1].replace(/[^0-9]/g, ''),
            ventas30dias[2].replace(/[^0-9]/g, ''),
            ventas30dias[3].replace(/[^0-9]/g, ''),
            ventas30dias[4].replace(/[^0-9]/g, ''),
            ventas30dias[5].replace(/[^0-9]/g, ''),
            ventas30dias[6].replace(/[^0-9]/g, ''),
            ventas30dias[7].replace(/[^0-9]/g, ''),
            ventas30dias[8].replace(/[^0-9]/g, ''),
            ventas30dias[9].replace(/[^0-9]/g, ''),
            ventas30dias[10].replace(/[^0-9]/g, ''),
            ventas30dias[11].replace(/[^0-9]/g, ''),
            ventas30dias[12].replace(/[^0-9]/g, ''),
            ventas30dias[13].replace(/[^0-9]/g, ''),
            ventas30dias[14].replace(/[^0-9]/g, ''),
            ventas30dias[15].replace(/[^0-9]/g, ''),
            ventas30dias[16].replace(/[^0-9]/g, ''),
            ventas30dias[17].replace(/[^0-9]/g, ''),
            ventas30dias[18].replace(/[^0-9]/g, ''),
            ventas30dias[19].replace(/[^0-9]/g, ''),
            ventas30dias[20].replace(/[^0-9]/g, ''),
            ventas30dias[21].replace(/[^0-9]/g, ''),
            ventas30dias[22].replace(/[^0-9]/g, ''),
            ventas30dias[23].replace(/[^0-9]/g, ''),
            ventas30dias[24].replace(/[^0-9]/g, ''),
            ventas30dias[25].replace(/[^0-9]/g, ''),
            ventas30dias[26].replace(/[^0-9]/g, ''),
            ventas30dias[27].replace(/[^0-9]/g, ''),
            ventas30dias[28].replace(/[^0-9]/g, ''),
            ventas30dias[29].replace(/[^0-9]/g, '')
            ],
            pointRadius: 5,
            pointHoverRadius: 10,
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgba(245, 66, 66)'
        }]
    },
    options:{
        //indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

