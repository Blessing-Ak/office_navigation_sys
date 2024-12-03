from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Example data for navigation
responses = {
    "collect transcript": "Do you want to verify your transcript or collect it?",
    "verify transcript": "Go to Room X. Directions: From the main gate, turn left and go to the first floor.",
    "collect transcript graduate": "Go to Room Y. Directions: From the admin block, climb to the second floor."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').lower()
    response = next((responses[key] for key in responses if key in query), 
                    "Sorry, I didn't understand your query. Please try again.")
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
