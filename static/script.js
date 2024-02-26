function showSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  const mainContent = document.querySelector("#main-content");
  if (sidebar.style.display === "flex") {
    hideSideBar(event);
  } else {
    sidebar.style.display = "flex";
    setTimeout(() => {
      sidebar.style.left = "0px";
    }, 0.1);
    // mainContent.style.marginLeft = "350px";
  }
  event.preventDefault();
}
function hideSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  const mainContent = document.querySelector("#main-content");
  sidebar.style.left = "-400px";
  console.log("Function called");
  setTimeout(() => {
    sidebar.style.display = "none";
  }, 500);
  setTimeout(() => {
    // mainContent.style.marginLeft = "200px";
  }, 20);
  event.preventDefault();
}
// var pos = document.documentElement;
// pos.addEventListener("mousemove",e=>{
//   pos.style.setProperty("--x",e.clientX+"px")
//   pos.style.setProperty("--y",e.clientY+"px")
// })
