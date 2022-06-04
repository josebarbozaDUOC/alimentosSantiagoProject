var isSidebarOpen = false;

function changeColors(){
  //Cambia el color del sidebar
  var colors = ['#dfbbbb', '#c7a3e0', '#e0a3d8', '#a3e0db', '#a3e0aa', '#dde0a3', '#dfbc9e'];
  var random_color = colors[Math.floor(Math.random() * colors.length)];
  document.getElementById('mySidepanel').style.backgroundColor = random_color;
}

//Set the width of the sidebar to 250px (show it)
function openNav() {
  //aparece el overlay y la sidebar
  document.getElementById("myNav").style.width = "100%";
  document.getElementById("mySidepanel").style.transform = "translate(-100%,0px)"
  changeColors();
  isSidebarOpen = true;
  //document.body.style.overflow =  'hidden';
}

  //Set the width of the sidebar to 0 (hide it)
function closeNav() {
  //se colapsan
  document.getElementById("myNav").style.width = "0%";
  document.getElementById("mySidepanel").style.transform = "translate(0px,0px)"
  isSidebarOpen = false;
}

// Al presionar la tecla ESCAPE cierra el sidebar
document.addEventListener('keydown', function(event){
	if(event.key === "Escape"){
    closeNav();
	}
})

//Cuando el click es fuera del sidebar se cierra
document.addEventListener('click', e => {
  const isSideBar = e.target.closest('[data-sidebar]')
  const isSidebarButton = e.target.matches("[data-sidebar-button]")

  if (isSidebarButton)
    return

  if (!isSideBar && isSidebarOpen)
    closeNav();

  /*
  //let currentSidebar
  if (isSideBar){
    //currentSidebar = e.target.closest('[data-sidebar]')
    //currentSidebar.classList.toggle('active')
    //pasan cosas
    changeColors();
  }
  else
    //document.getElementById('mySidepanel').style.backgroundColor = 'black';
    if (isSidebarOpen)
      closeNav();*/
})