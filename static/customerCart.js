document.querySelector(".studentCart").addEventListener("click", (event) => {
  const sidebar = document.querySelector(".sidebar");
  const isButton = event.target.classList.contains("show_button");
  // Check if the clicked element is not within the sidebar
  if (!sidebar.contains(event.target) && !isButton) {
    sidebar.style.left = "-400px";
    console.log("Function called");
    setTimeout(() => {
      sidebar.style.display = "none";
    }, 500);
    // setTimeout(() => {
    //   mainContent.style.marginLeft = "400px";
    // }, 20);
  }
});
function showSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  const body = document.querySelector("body");
  if (sidebar.style.display === "flex") {
    hideSideBar(event);
  } else {
    sidebar.style.display = "flex";
    sidebar.style.position = "fixed";
    sidebar.style.left = "0px";
    body.style.overflowY = "hidden"; // Disable vertical scrolling of the body
  }
  event.preventDefault();
}

function hideSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  const body = document.querySelector("body");
  sidebar.style.left = "-400px";
  setTimeout(() => {
    sidebar.style.display = "none";
    body.style.overflowY = "auto"; // Enable vertical scrolling of the body
  }, 500);
  event.preventDefault();
}
