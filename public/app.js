const dataForm = document.getElementById('data-form');
const currentTimeElement = document.getElementById('current-time');

function getCurrentTimePoint() {
    const now = new Date();
    const hour = now.getHours();
    const minute = now.getMinutes();

    if (hour < 7 || (hour === 7 && minute < 45)) return "wakeUp"; if (hour < 10 || (hour === 10 && minute < 45))
        return "7_45am"; if (hour < 12) return "10_45am"; if (hour < 15) return "12pm"; if (hour < 18) return "3pm"; if
        (hour < 20 || (hour === 20 && minute < 30)) return "6pm"; return "8_30pm";
} function renderFormFields(timePoint) {
    let fields = ''; if (timePoint === "wakeUp") {
        fields += ` <div>
    <label for="weight">Weight:</label>
    <input type="number" id="weight" name="weight">
    </div>
    `;
    }

    fields += `
    <div>
        <label for="mood">Mood:</label>
        <select id="mood" name="mood">
            <option value="M-">M-</option>
            <option value="M">M</option>
            <option value="M+">M+</option>
        </select>
    </div>
    <div>
        <label for="goals">Goals:</label>
        <select id="goals" name="goals">
            <option value="G-">G-</option>
            <option value="G">G</option>
            <option value="G+">G+</option>
        </select>
    </div>
    <div>
        <label for="food_quality">Food Quality:</label>
        <select id="food_quality" name="food_quality">
            <option value="L">L</option>
            <option value="M">M</option>
            <option value="H">H</option>
        </select>
    </div>
    `;

    dataForm.innerHTML = fields;
}

function displayCurrentTime(timePoint) {
    const currentTime = new Date().toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });

    currentTimeElement.textContent = `Current Time (${timePoint}): ${currentTime}`;
}

function setupForm() {
    const currentTimePoint = getCurrentTimePoint();
    renderFormFields(currentTimePoint);
    displayCurrentTime(currentTimePoint);
}

setupForm();

const submitFormButton = document.getElementById('submit-form-button');

submitFormButton.addEventListener('click', async (event) => {
    event.preventDefault();

    const weightElement = document.getElementById('weight');
    const weight = weightElement ? weightElement.value : null;
    const mood = document.getElementById('mood').value;
    const goals = document.getElementById('goals').value;
    const foodQuality = document.getElementById('food_quality').value;
    const timePoint = getCurrentTimePoint();
    const currentTime = new Date();

    // Prepare the form data to send to the server
    const formData = {
        weightAM: weight,
        mood: mood,
        goals: goals,
        foodQuality: foodQuality,
        time: timePoint,
        // currentTime,
    };

    try {
        // Send the form data to the server using a POST request
        const response = await fetch('/submit-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        console.log(JSON.stringify(formData));

        // Check if the request was successful and handle the response
        if (response.ok) {
            const result = await response.json();
            console.log(result.message);
        } else {
            console.error('Error submitting data:', response.statusText);
        }
    } catch (error) {
        console.error('Error submitting data:', error);
    }
});