// REDIRECTS USER
function redirectTo(route) {
  window.location.href = route;
}

// CLOSE FLASH BUTTONS
const flashCloseBtns = document.querySelectorAll(".flash-close-btn");

for (let i = 0; i < flashCloseBtns.length; i++) {
  const flashCloseBtn = flashCloseBtns[i];
  const flashContainer = document.querySelector(".flash-container");
  flashCloseBtn.addEventListener("click", function () {
    flashContainer.style.display = "none";
  });
}
