function deletePost(postId) {
  fetch("/timeline/delete-post/postId=" + postId, {
    method: "DELETE",
  })
    .then((response) => response.text())
    .then((data) => {
      alert(data);
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
