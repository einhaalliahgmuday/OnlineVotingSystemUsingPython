// AUTO-RESIZE TEXTAREA FOR POST FORM
document.getElementById("post-text").addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// DELETE POST
function deletePost(postId) {
  fetch("/timeline/delete-post/postId=" + postId, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success == false) {
        alert(data.message);
      } else if (data.success) {
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// DISPLAY FILE NAME
document.getElementById("post-image").addEventListener("change", function () {
  const fileName = document.querySelector(".file-name");
  fileName.textContent = this.files[0].name;
});
