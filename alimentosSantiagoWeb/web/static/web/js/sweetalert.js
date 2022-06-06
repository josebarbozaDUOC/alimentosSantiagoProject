
//mensajes de confirmación en la esquina superior derecha
function sweetMensaje(mensaje){
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 1500,
        timerProgressBar: false,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })
        
        Toast.fire({
        icon: 'success',
        title: mensaje,
        hideClass: {
            popup: 'animate__animated animate__zoomOutRight'
        }
    })
}

function pedidoExitoso(){
    let timerInterval
    Swal.fire({
    icon: 'success',
    title: '¡Felicidades!',
    text: "Tu pedido se está preparando, llegará: ",
    allowOutsideClick: false,
    timer: 4000,
    timerProgressBar: true,
    showClass: {
        popup: 'animate__animated animate__tada'
    },
    hideClass: {
        popup: 'animate__animated animate__bounceOutRight'
    },
    didOpen: () => {
        Swal.showLoading()
        const b = Swal.getHtmlContainer().querySelector('b')
        timerInterval = setInterval(() => {
        b.textContent = Swal.getTimerLeft()
        }, 100)
    },
    willClose: () => {
        clearInterval(timerInterval)
    }
    }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer')
        window.location.href = '/perfil-usuario/'
    }
    })
}

//eliminar un producto del listado de productos | solo personal con permiso
function eliminarProducto(id){
    /*console.log(id)*/
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡Esta acción no se puede deshacer!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        confirmButtonText: '¡Si, eliminar!',
        cancelButtonText: 'No, cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/eliminar-producto/'+id+'/'
        }
    })
}