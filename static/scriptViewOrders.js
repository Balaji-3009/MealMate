document.querySelector(".upload_menu").addEventListener("click", (event) => {
  const sidebar = document.querySelector(".sidebar");
  // const mainContent = document.querySelector(".upload_form");
  const isButton = event.target.classList.contains("show_button");
  // Check if the clicked element is not within the sidebar
  if (!sidebar.contains(event.target) && !isButton) {
    sidebar.style.left = "-400px";
    console.log("Function called");
    setTimeout(() => {
      sidebar.style.display = "none";
    }, 500);
    setTimeout(() => {
      // mainContent.style.marginLeft = "400px";
    }, 20);
  }
  // No need for event.preventDefault() if you want normal click behavior
});
function showSideBar(event) {
  // const mainContent = document.querySelector(".upload_form");
  const sidebar = document.querySelector(".sidebar");
  if (sidebar.style.display === "flex") {
    hideSideBar(event);
  } else {
    sidebar.style.display = "flex";
    setTimeout(() => {
      sidebar.style.left = "0px";
    }, 0.1);
    // mainContent.style.marginLeft = "500px";
  }
  event.preventDefault();
}
function hideSideBar(event) {
  // const mainContent = document.querySelector(".upload_form");
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.left = "-400px";
  // console.log("Function called");
  setTimeout(() => {
    sidebar.style.display = "none";
  }, 500);
  setTimeout(() => {
    // mainContent.style.marginLeft = "400px";
  }, 20);
  event.preventDefault();
}