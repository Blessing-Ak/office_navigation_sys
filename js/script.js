document.getElementById('search-button').addEventListener('click', handleSearch);

function handleSearch() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const output = document.getElementById('output');

    // Example queries and responses
    const responses = {
        "collect transcript": "Do you want to verify your transcript or collect it?",
        "verify transcript": "Go to Room X. Directions: From the main gate, turn left and go to the first floor.",
        "collect transcript graduate": "Go to Room Y. Directions: From the admin block, climb to the second floor."
    };

    // Check if query exists in responses
    const response = Object.keys(responses).find(key => query.includes(key));

    if (response) {
        output.textContent = responses[response];
    } else {
        output.textContent = "Sorry, I didn't understand your query. Please try again.";
    }
}

