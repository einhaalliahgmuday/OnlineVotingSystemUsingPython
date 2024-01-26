function redirectTo(route) {
  window.location.href = route;
}

// Create & Edit Ballot JavaScript
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

  fetch('/get-ballot-status')
    .then(response => response.json())
    .then(data => {

      if (data.success) {
        const isOpen = data.isOpen;

        const statusElement = document.getElementById('ballot-status');

        if (isOpen) {
          statusElement.innerText = 'Voting is now open.';
        } else {
          statusElement.innerText = 'Voting is now closed.';
        }
      } else {
        console.error('Failed to fetch ballot status');
      }
    })
    .catch(error => {
      console.error('Error fetching ballot status:', error);
    });

    const studentIdInput = document.getElementById('studentId');
  const nameElement = document.getElementById('candidateName');
  const courseElement = document.getElementById('candidateCourse');

  studentIdInput.addEventListener('blur', async function () {
    const studentId = this.value;

    if (studentId) {
      try {
        const response = await fetch(`/check_existing_candidate/${studentId}`);
        const data = await response.json();

        if (data.exists) {
          alert(`Student ID ${studentId} is already a candidate. Please enter a different student ID.`);
        } else {

          fetch(`/get_student_info/${studentId}`)
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                const studentData = data.data;
                nameElement.innerText = `Name: ${studentData.name.first} ${studentData.name.last}`;
                courseElement.innerText = `Course: ${studentData.course}`;
              } else {
                nameElement.innerText = '';
                courseElement.innerText = '';
                alert(`Error: ${data.message}`);
              }
            })
            .catch(error => {
              console.error('Error fetching student info:', error);
            });
        }
      } catch (error) {
        console.error('Error checking existing candidate:', error);
      }
    } else {
      nameElement.innerText = '';
      courseElement.innerText = '';
    }
  });

});

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
        const studentData = data.data;
        nameElement.innerText = `Name: ${studentData.name.first} ${studentData.name.last}`;
        courseElement.innerText = `Course: ${studentData.course}`;
      } else {
        nameElement.innerText = '';
        courseElement.innerText = '';
        alert(data.message); 
      }
    })
    .catch(error => {
      console.error('Error fetching student info:', error);
    });

}

const enteredStudentIds = new Map();

async function checkForDuplicates(studentId, position, index) {
  try {

    const response = await fetch(`/check_duplicate/${studentId}/${position}/${index}`);
    const data = await response.json();

    if (data.isDuplicate) {
      if (data.isExistInOtherPosition) {
        alert(`Student ID ${studentId} already exists in another position. Please change it to avoid errors.`);
      } else {
        alert(`Duplicate student ID is detected for ${position} ${index}. Please change it to avoid errors.`);
      }
    } else {
      
      const existingEntries = enteredStudentIds.get(studentId);

      if (existingEntries && existingEntries.some(entry => entry.position === position && entry.index !== index)) {
        alert(`Student ID ${studentId} already exists in the same position for a different index. Please change it to avoid errors.`);
      } 
      else if (existingEntries && existingEntries.some(entry => entry.position !== position)) {
        alert(`Student ID ${studentId} already exists in another position. Please change it to avoid errors.`);
      } 
      else {
        
        if (!existingEntries) {
          enteredStudentIds.set(studentId, [{ position, index }]);
        } else {
          existingEntries.push({ position, index });
        }

        fetch(`/get_student_info/${studentId}`)
          .then(response => response.json())
          .then(data => {
            if (!data.success) {
              alert(`Student ID ${studentId} does not belong to any student. Please enter a valid student ID.`);
            }
          })
          .catch(error => {
            console.error('Error checking student existence:', error);
          });

        fetchStudentInfo(studentId, position, index);
      }
    }
  } catch (error) {
    console.error('Error checking for duplicates:', error);
  }
}

