function deleteCandidate(studentId) {
  fetch("/ballot/delete-candidate/" + studentId, {
    method: "DELETE",
  })
    .then((response) => response.text())
    .then(() => {
      alert(`Candidate successfully deleted.`);
      window.location.reload();
    })

    .catch((error) => {
      console.error("Error:", error);
    });
}

function toggleState() {
  var statusElement = document.getElementById("status");

  var currentStatus = statusElement.innerText.trim();
  var action = currentStatus === "STATUS: NEW" ? "open" : "close";

  fetch("/ballot/status", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "action=" + action,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.reload();
      } else {
        console.error("Error updating ballot status");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function clearBallot() {
  var ballotStatus = document.getElementById("status").innerText.trim();

  if (ballotStatus === "STATUS: CLOSED") {
    // Ask for confirmation
    var confirmation = confirm(
      "Are you sure you want to clear the ballot? This action cannot be undone."
    );

    if (confirmation) {
      fetch("/clear-ballot", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.reload();
          } else {
            alert("An error occured. Please try again later.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      alert("Clear ballot action canceled.");
    }
  } else if (ballotStatus === "STATUS: OPEN") {
    alert("Cannot clear the ballot. Please close the ballot first.");
  }
}
