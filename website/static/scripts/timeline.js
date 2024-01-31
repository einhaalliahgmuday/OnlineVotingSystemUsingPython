// AUTO-RESIZE TEXTAREA
function autoResize(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
}

// DELETE POST
function deletePost(postId) {
  fetch("/timeline/delete-post/postId=" + postId, {
    method: "DELETE",
  })
    .then((_res) => {
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// DISPLAY FILE NAME
function displayFileName(input) {
  const fileName = document.querySelector(".file-name");
  fileName.textContent = input.files[0].name;
}
