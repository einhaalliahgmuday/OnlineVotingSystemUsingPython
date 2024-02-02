// REDIRECTS USER
function redirectTo(route) {
  window.location.href = route;
}

// CLOSE FLASH MESSAGES DIV
const flashCloseBtns = document.querySelectorAll(".flash-close-btn");

for (let i = 0; i < flashCloseBtns.length; i++) {
  const flashCloseBtn = flashCloseBtns[i];
  const flashContainer = document.querySelector(".flash-container");
  flashCloseBtn.addEventListener("click", function () {
    flashContainer.style.display = "none";
  });
}

// LOGOUT
const logoutBtn = document.getElementById("logoutButton");

if (logoutBtn) {
  logoutBtn.addEventListener("click", function () {
    var confirmLogout = confirm("Are you sure you want to logout?");

    if (confirmLogout) {
      window.location.href = "/logout";
    }
  });
}
