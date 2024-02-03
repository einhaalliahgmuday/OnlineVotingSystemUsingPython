// DELETE CANDIDATE FROM THE BALLOT
function deleteCandidate(studentId) {
  fetch("/ballot/delete-candidate/" + studentId, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        alert("An error occured. Please try again later.");
        console.error(data.message);
      }
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// TOGGLE THE BALLOT STATUS
function toggleState() {
  let statusElement = document.getElementById("status");

  let currentStatus = statusElement.innerText.trim();
  let action = currentStatus === "STATUS: NEW" ? "open" : "close";

  fetch("/ballot/status", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "action=" + action,
  })
    .then((response) => response.json())
    .then(() => {
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// CLEAR THE BALLOT
function clearBallot() {
  let ballotStatus = document.getElementById("status").innerText.trim();

  if (ballotStatus === "STATUS: NEW" || ballotStatus === "STATUS: CLOSED") {
    var confirmation = confirm(
      "Are you sure you want to clear the ballot? This action cannot be undone."
    );

    if (confirmation) {
      fetch("/ballot/clear-ballot", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) {
            alert("An error occured. Please try again later.");
            console.error(data.message);
          }
          window.location.reload();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  } else if (ballotStatus === "STATUS: OPEN") {
    alert("Cannot clear the ballot. Please close the ballot first.");
  }
}
