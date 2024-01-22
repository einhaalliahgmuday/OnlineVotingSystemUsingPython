function redirectTo(route) {
  window.location.href = route;
}

//Create Ballot JavaScript
function fetchStudentInfo(studentId, position, index) {
  const nameElement = document.getElementById(`${position}_name_${index}`);
  const courseElement = document.getElementById(`${position}_course_${index}`);

  if (!studentId) {
    nameElement.innerText = '';
    courseElement.innerText = '';
    return;
  }

  fetch(`/get_student_info/${studentId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        nameElement.innerText = `Name: ${data.name}`;
        courseElement.innerText = `Course: ${data.course}`;
      } 
      else {
        nameElement.innerText = '';
        courseElement.innerText = '';
      }
    })
    .catch(error => {
      console.error('Error fetching student info:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
  const positions = [
    'president', 'vice_president', 'executive_board_sec', 'vp_finance',
    'vp_academic_affairs', 'vp_internal_external_affairs', 'vp_public_relations',
    'vp_research_dev', 'first_yr_rep', 'second_yr_rep', 'third_yr_rep', 'fourth_yr_rep'
  ];

  let lastFocusedInput = null; 

  positions.forEach(position => {
    for (let i = 1; i <= 4; i++) {
      const inputElement = document.getElementById(`${position}_id${i}`);
      if (inputElement) {
        inputElement.addEventListener('focus', function () {
          lastFocusedInput = this; 
        });

        inputElement.addEventListener('blur', function () {
          const studentId = this.value;
          const index = i;
          const positionName = position;

          if (this !== lastFocusedInput) {
            return;
          }

          checkForDuplicates(studentId, positionName, index);

          fetchStudentInfo(studentId, positionName, index);
        });
      }
    }
  });

});

const enteredStudentIds = new Map();

function checkForDuplicates(studentId, position, index) {

  if (enteredStudentIds.has(studentId)) {
    const existingPositions = enteredStudentIds.get(studentId);

    if (existingPositions.includes(position)) {
      alert(`Duplicate student ID is detected for ${position} ${index}.
      Please change it to avoid errors.`);
    } 
    else {
      alert(`Student ID ${studentId} already exists in another position.
      Please change it to avoid errors.`);
    }
  } 
  else {
    
    fetch(`/get_student_info/${studentId}`)
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert(`Student ID ${studentId} does not belong to any student.
          Please enter a valid student ID.`);
        } 
        else {
          enteredStudentIds.set(studentId, [position]);
        }
      })
      .catch(error => {
        console.error('Error checking student existence:', error);
      });
  }

  fetchStudentInfo(studentId, position, index);
}
