document.addEventListener("DOMContentLoaded", function() {
    var path = window.location.pathname;
    var page = path.split("/").pop().split(".")[0];
    document.body.classList.add(page);
});
