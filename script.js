document.getElementById('studentForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent actual form submission

    const studentId = document.getElementById('studentId').value.trim();
    console.log('Student ID Entered:', studentId); // Debugging line
    console.log('Students Data:', studentsData); // Debugging line

    const student = studentsData.find(row => row[0].toString() === studentId); // Convert ID to string for comparison

    const studentDetailsDiv = document.getElementById('studentDetails');
    if (student) {
        studentDetailsDiv.innerHTML = `
            <h2>Details for Student ID: ${student[0]}</h2>
            <p><strong>Name:</strong> ${student[1]}</p>  <!-- Assuming Name is in the second column -->
            <p><strong>Age:</strong> ${student[2]}</p>   <!-- Assuming Age is in the third column -->
            <p><strong>Course:</strong> ${student[3]}</p> <!-- Assuming Course is in the fourth column -->
        `;
    } else {
        studentDetailsDiv.innerHTML = <p style="color: red;">No student found with ID: ${studentId}</p>;
    }

        });
