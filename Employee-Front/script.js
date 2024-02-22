function showSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "flex";
  event.preventDefault();
}
function hideSideBar(event) {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "none";
  event.preventDefault();
}