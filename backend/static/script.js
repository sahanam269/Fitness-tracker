// Add activity

function addActivity() {

    const name = document.getElementById("name").value;
    const activity = document.getElementById("activity").value;
    const duration = document.getElementById("duration").value;
    const steps = document.getElementById("steps").value;
    const date = document.getElementById("date").value;


    // Check fields

    if (name === "" ||
        activity === "" ||
        duration === "" ||
        steps === "" ||
        date === "") {

        alert("Please fill all fields.");
        return;
    }


    // Send data to Flask backend

    fetch("/add_activity", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,
            activity: activity,
            duration: duration,
            steps: steps,
            date: date

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        // Clear form

        document.getElementById("name").value = "";
        document.getElementById("activity").value = "";
        document.getElementById("duration").value = "";
        document.getElementById("steps").value = "";
        document.getElementById("date").value = "";

        // Reload activities

        loadActivities();

    })

    .catch(error => {

        console.error(error);

        alert("Something went wrong.");

    });

}



// Load activities

function loadActivities() {

    fetch("/activities")

    .then(response => response.json())

    .then(data => {

        const table =
            document.getElementById("activityTable");

        table.innerHTML = "";

        let totalSteps = 0;
        let totalDuration = 0;


        data.forEach(activity => {

            totalSteps += Number(activity.steps);

            totalDuration += Number(activity.duration);


            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${activity.name}</td>
                <td>${activity.activity}</td>
                <td>${activity.duration} min</td>
                <td>${activity.steps}</td>
                <td>${activity.date}</td>
            `;

            table.appendChild(row);

        });


        // Update dashboard

        document.getElementById("totalSteps").textContent =
            totalSteps;

        document.getElementById("totalDuration").textContent =
            totalDuration + " min";

        document.getElementById("totalActivities").textContent =
            data.length;

    })

    .catch(error => {

        console.error(error);

    });

}
function loadStreak() {
    fetch("/streak")
    .then(response => response.json())
    .then(data => {
        document.getElementById("currentStreak").textContent =
            data.streak + (data.streak === 1 ? " day" : " days");
    })
    .catch(error => console.error(error));
}



// Load data when page opens

loadActivities();
loadStreak();
function checkDailyReminder() {
    fetch("/activities")
    .then(response => response.json())
    .then(data => {

        const today = new Date().toISOString().split("T")[0];

        const completedToday = data.some(activity => activity.date === today);

        if (!completedToday) {
            alert("🔔 Reminder: Don't forget to complete your fitness activity today!");
        }
    })
    .catch(error => console.error(error));
}

checkDailyReminder();
loadActivities();
loadStreak();
checkDailyReminder();
