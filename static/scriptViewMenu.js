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
  console.log("Function called");
  setTimeout(() => {
    sidebar.style.display = "none";
  }, 500);
  setTimeout(() => {
    // mainContent.style.marginLeft = "400px";
  }, 20);
  event.preventDefault();
}
