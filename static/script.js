function showSideBar(event) {
    const sidebar = document.querySelector(".sidebar");
  
    sidebar.style.display = "flex";
    setTimeout(() => {
      sidebar.style.left = "0px";
    }, 0.1);
  
    event.preventDefault();
  }
  function hideSideBar(event) {
    const sidebar = document.querySelector(".sidebar");
    sidebar.style.left = "-500px";
    console.log("Function called");
    setTimeout(() => {
      sidebar.style.display = "none";
    }, 1000);
  
    event.preventDefault();
  }
  // var pos = document.documentElement;
  // pos.addEventListener("mousemove",e=>{
  //   pos.style.setProperty("--x",e.clientX+"px")
  //   pos.style.setProperty("--y",e.clientY+"px")
  // })