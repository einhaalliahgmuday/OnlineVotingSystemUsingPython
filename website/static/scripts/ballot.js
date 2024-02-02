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
  var statusElement = document.getElementById('status');
  var openBtn = document.getElementById('open-btn');
  var clearBtn = document.getElementById('clear-btn');

  var currentStatus = statusElement.innerText.trim();
  var action = currentStatus === 'STATUS: NEW' ? 'open' : 'close';  // Determine the action based on the current status

  fetch("/ballot/status", {
      method: "POST",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded",  // Set the content type to 'application/x-www-form-urlencoded'
      },
      body: "action=" + action,  // Pass the action as part of the request body
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
  var ballotStatus = document.getElementById('status').innerText.trim();

  if (ballotStatus === 'STATUS: CLOSED') {
      fetch("/clear-ballot", {
          method: "POST",
      })
          .then((response) => response.json())
          .then((data) => {
              if (data.success) {
                  alert('Ballot is cleared successfully.');
                  window.location.reload();
              } else {
                  console.error("Error clearing ballot");
              }
          })
          .catch((error) => {
              console.error("Error:", error);
          });
  } else {
      alert('Cannot clear the ballot. Please close the ballot first.');
  }
}