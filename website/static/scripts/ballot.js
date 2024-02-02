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

  // Assuming you have an element with id 'status' for displaying the status
  var currentStatus = statusElement.innerText.trim();

  fetch("/update-ballot-status", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ currentStatus }),
  })
      .then((response) => response.json())
      .then((data) => {
          if (data.success) {
              if (currentStatus === "STATUS: NEW") {
                  statusElement.innerText = 'STATUS: OPEN';
                  openBtn.innerText = 'CLOSE BALLOT';
                  openBtn.setAttribute('data-action', 'close');
                  clearBtn.removeAttribute('disabled');
              } else if (currentStatus === "STATUS: OPEN") {
                  statusElement.innerText = 'STATUS: CLOSED';
                  openBtn.setAttribute('disabled', 'true');
              } else if (currentStatus === "STATUS: CLOSED") {
                  statusElement.innerText = 'STATUS: NEW';
                  openBtn.innerText = 'OPEN BALLOT';
                  openBtn.setAttribute('data-action', 'open');
                  clearBtn.setAttribute('disabled', 'true');
              }
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
      // Allow clearing the ballot
      // Add logic to clear the ballot and perform other actions if needed
      alert('Ballot is cleared.');
  } else {
      alert('Cannot clear the ballot. Please close the ballot first.');
  }
}