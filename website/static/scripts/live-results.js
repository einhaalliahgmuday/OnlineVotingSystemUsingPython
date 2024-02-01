setInterval(function () {
  document.getElementById("liveTime").textContent = new Date().toLocaleString();
}, 1000);

document.getElementById("liveTime").textContent = new Date().toLocaleString();

var socket = io("http://127.0.0.1:5000");

socket.on("vote", function (data) {
  // UPDATE RESULT FOR PRESIDENT WHEN A USER VOTES
  if (data.president.candidates.length > 0) {
    for (let i = 0; i < data.president.candidates.length; i++) {
      const candidate = data.president.candidates[i];
      const resultBar = document.querySelector(
        ".president-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("president-bar-abstain");
    abstain.style.width = `${data.president.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR EXECUTIVE VICE PRESIDENT WHEN A USER VOTES
  if (data.executive_vp.candidates.length > 0) {
    for (let i = 0; i < data.executive_vp.candidates.length; i++) {
      const candidate = data.executive_vp.candidates[i];
      const resultBar = document.querySelector(
        ".executive-vp-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("executive-vp-bar-abstain");
    abstain.style.width = `${data.executive_vp.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR EXECUTIVE BOARD SECRETARY WHEN A USER VOTES
  if (data.executive_board_sec.candidates.length > 0) {
    for (let i = 0; i < data.executive_board_sec.candidates.length; i++) {
      const candidate = data.executive_board_sec.candidates[i];
      const resultBar = document.querySelector(
        ".executive-board-sec-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("executive-board-sec-bar-abstain");
    abstain.style.width = `${data.executive_board_sec.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR FINANCE WHEN A USER VOTES
  if (data.vp_finance.candidates.length > 0) {
    for (let i = 0; i < data.vp_finance.candidates.length; i++) {
      const candidate = data.vp_finance.candidates[i];
      const resultBar = document.querySelector(
        ".vp-finance-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-finance-bar-abstain");
    abstain.style.width = `${data.vp_finance.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR ACADEMIC AFFAIRS WHEN A USER VOTES
  if (data.vp_academic_affairs.candidates.length > 0) {
    for (let i = 0; i < data.vp_academic_affairs.candidates.length; i++) {
      const candidate = data.vp_academic_affairs.candidates[i];
      const resultBar = document.querySelector(
        ".vp-academic-affairs-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-academic-affairs-bar-abstain");
    abstain.style.width = `${data.vp_academic_affairs.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR INTERNAL AFFAIRS WHEN A USER VOTES
  if (data.vp_internal_affairs.candidates.length > 0) {
    for (let i = 0; i < data.vp_internal_affairs.candidates.length; i++) {
      const candidate = data.vp_internal_affairs.candidates[i];
      const resultBar = document.querySelector(
        ".vp-internal-affairs-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-internal-affairs-bar-abstain");
    abstain.style.width = `${data.vp_internal_affairs.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR EXTERNAL AFFAIRS WHEN A USER VOTES
  if (data.vp_external_affairs.candidates.length > 0) {
    for (let i = 0; i < data.vp_external_affairs.candidates.length; i++) {
      const candidate = data.vp_external_affairs.candidates[i];
      const resultBar = document.querySelector(
        ".vp-external-affairs-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-external-affairs-bar-abstain");
    abstain.style.width = `${data.vp_external_affairs.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR PUBLIC RELATIONS WHEN A USER VOTES
  if (data.vp_public_relations.candidates.length > 0) {
    for (let i = 0; i < data.vp_public_relations.candidates.length; i++) {
      const candidate = data.vp_public_relations.candidates[i];
      const resultBar = document.querySelector(
        ".vp-public-relations-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-public-relations-bar-abstain");
    abstain.style.width = `${data.vp_public_relations.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR VICE PRESIDENT FOR RESEARCH AND DEVELOPMENT WHEN A USER VOTES
  if (data.vp_research_dev.candidates.length > 0) {
    for (let i = 0; i < data.vp_research_dev.candidates.length; i++) {
      const candidate = data.vp_research_dev.candidates[i];
      const resultBar = document.querySelector(
        ".vp-research-dev-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("vp-research-dev-bar-abstain");
    abstain.style.width = `${data.vp_research_dev.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR FIRST YEAR REPRESENTATIVE WHEN A USER VOTES
  if (data.first_yr_rep.candidates.length > 0) {
    for (let i = 0; i < data.first_yr_rep.candidates.length; i++) {
      const candidate = data.first_yr_rep.candidates[i];
      const resultBar = document.querySelector(
        ".first-yr-rep-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("first-yr-rep-bar-abstain");
    abstain.style.width = `${data.first_yr_rep.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR SECOND YEAR REPRESENTATIVE WHEN A USER VOTES
  if (data.second_yr_rep.candidates.length > 0) {
    for (let i = 0; i < data.second_yr_rep.candidates.length; i++) {
      const candidate = data.second_yr_rep.candidates[i];
      const resultBar = document.querySelector(
        ".second-yr-rep-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("second-yr-rep-bar-abstain");
    abstain.style.width = `${data.second_yr_rep.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR THIRD YEAR REPRESENTATIVE WHEN A USER VOTES
  if (data.third_yr_rep.candidates.length > 0) {
    for (let i = 0; i < data.third_yr_rep.candidates.length; i++) {
      const candidate = data.third_yr_rep.candidates[i];
      const resultBar = document.querySelector(
        ".third-yr-rep-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("third-yr-rep-bar-abstain");
    abstain.style.width = `${data.third_yr_rep.abstain.votePercentage}%`;
  }

  // UPDATE RESULT FOR FOURTH YEAR REPRESENTATIVE WHEN A USER VOTES
  if (data.fourth_yr_rep.candidates.length > 0) {
    for (let i = 0; i < data.fourth_yr_rep.candidates.length; i++) {
      const candidate = data.fourth_yr_rep.candidates[i];
      const resultBar = document.querySelector(
        ".third-yr-rep-bar-candidate[data-student-id='" +
          candidate.studentId +
          "']"
      );
      resultBar.style.width = `${candidate.votePercentage}%`;
    }
    const abstain = document.getElementById("third-yr-rep-bar-abstain");
    abstain.style.width = `${data.fourth_yr_rep.abstain.votePercentage}%`;
  }
});
