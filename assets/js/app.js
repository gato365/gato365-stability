const dataForm = document.getElementById('data-form');
const currentTimeElement = document.getElementById('current-time');

function getCurrentTimePoint() {
    const now = new Date();
    now.setHours(7, 45);
    const hour = now.getHours();
    const minute = now.getMinutes();


  

 


    if (hour < 7 || (hour === 7 && minute < 45)) return "wakeUp"; if (hour < 10 || (hour === 10 && minute < 45))
        return "7_45am"; if (hour < 12) return "10_45am"; if (hour < 15) return "12pm"; if (hour < 18) return "3pm"; if
        (hour < 20 || (hour === 20 && minute < 30)) return "6pm"; return "8_30pm";
} function renderFormFields(timePoint) {
    let fields = '';

    if (timePoint === "wakeUp") {
        fields += `
        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weight">Weight:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" id="weight" name="weight">
        </div>
        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="myYFourLife">My Why For Life:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="myYFourLife" name="myYFourLife">
        </div>
        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="myYFourKelley">My Why For Kelley:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="myYFourKelley" name="myYFourKelley">
        </div>


        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="myYFourGATO365">My Why For GATO365:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="myYFourGATO365" name="myYFourGATO365">
        </div>
        
        
        
        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="numberOfDays">Number of Days:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" id="numberOfDays" name="numberOfDays">
        </div>   
        <div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="blessings">Blessings:</label>
    <textarea class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="blessings" name="blessings"></textarea>
</div>
        
<hr class="border-t border-black-400 my-8">  
    `;
    }

    fields += `
    <div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="mood">Mood:</label>
    <select class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="mood" name="mood">
        <option value="M-">M-</option>
        <option value="M">M</option>
        <option value="M+">M+</option>
    </select>
</div>
<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="goals">Goals:</label>
    <select class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="goals" name="goals">
        <option value="G-">G-</option>
        <option value="G">G</option>
        <option value="G+">G+</option>
    </select>
</div>
<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="food_quality">Food Quality:</label>
    <select class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="food_quality" name="food_quality">
        <option value="L">L</option>
        <option value="M">M</option>
        <option value="H">H</option>
    </select>
</div>
<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="MJ">MJ:</label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" id="MJ" name="MJ">
</div>
<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="alcohol">Alcohol:</label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" id="alcohol" name="alcohol">
</div>
<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="eatingOut">Eating Out:</label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" id="eatingOut" name="eatingOut">
</div>

<div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="notes">Notes:</label>
    <textarea class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="notes" name="notes"></textarea>
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

    const timePoint = getCurrentTimePoint();
    const currentTime = new Date();

    // Prepare the form data to send to the server
    const formData = {
        weightAM: document.getElementById('weight')?.value,
        myYFourLife: document.getElementById('myYFourLife')?.value,
        myYFourKelley: document.getElementById('myYFourKelley')?.value,
        myYFourGATO365: document.getElementById('myYFourGATO365')?.value,
        numberOfDays: document.getElementById('numberOfDays')?.value,
        mood: document.getElementById('mood')?.value,
        goals: document.getElementById('goals')?.value,
        foodQuality: document.getElementById('food_quality')?.value,
        MJ: document.getElementById('MJ')?.value,
        alcohol: document.getElementById('alcohol')?.value,
        eatingOut: document.getElementById('eatingOut')?.value,
        blessings: document.getElementById('blessings')?.value,
        notes: document.getElementById('notes')?.value,
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
