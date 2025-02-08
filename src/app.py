import os
from dotenv import load_dotenv
import datetime
from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)

# Initialize a simple in-memory storage for notes
notes = {}

# Initialize a variable to store AI Insights (to be cleared each time)
ai_insights = ""

# Load environment variables from the .env file
load_dotenv()

# Hugging Face API key and URL for sentiment analysis model
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = "google/gemma-2-2b-it"

@app.route('/')
def index():
    # Render the main page, which will show the list of notes and AI insights
    return render_template('index.html', notes=notes, ai_insights=ai_insights)

@app.route('/new_note', methods=['POST'])
def new_note():
    # Create a new note ID and initialize an empty list for the note
    note_id = str(len(notes) + 1)
    notes[note_id] = []
    return jsonify({'note_id': note_id})

@app.route('/add_message', methods=['POST'])
def add_message():
    note_id = request.form['note_id']
    message = request.form['message']

    # Get the current timestamp in a human-readable format
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    if note_id in notes:
        notes[note_id].append({'message': message, 'timestamp': timestamp})
        return jsonify({'success': True, 'timestamp': timestamp})

    return jsonify({'success': False})

@app.route('/delete_message', methods=['POST'])
def delete_message():
    note_id = request.form['note_id']
    message_index = int(request.form['message_index'])

    if note_id in notes and len(notes[note_id]) > message_index:
        notes[note_id].pop(message_index)
        return jsonify({'success': True})

    return jsonify({'success': False})

@app.route('/summarize', methods=['POST'])
def summarize():
    global ai_insights  # Reference the global AI Insights variable
    ai_insights = ""  # Clear any previous insights when the user requests new ones

    note_id = request.form['note_id']
    if note_id in notes:
        # Join all messages to summarize them
        text_to_analyze = "\n".join([f"{msg['timestamp']}: {msg['message']}" for msg in notes[note_id]])

        prompt = f"""
            Below are the user's notes:

            {text_to_analyze}

            Based on the sentiments in these notes, explain to the user what they are feeling and their mood. Provide actionable advice to help the user improve their emotional well-being. Be practical and offer specific suggestions that can help them feel better.
            """

        # Call Hugging Face API
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
                headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
                json={"inputs": prompt},
            )

            print(f"Response Content: {response.text}")

            # Check if the response was successful
            if response.status_code == 200:
                result = response.json()
                print(f"Full API Response: {result}")

                # Isolate the generated text from the API response
                if isinstance(result, list) and len(result) > 0:
                    full_summary = result[0].get("generated_text", "Could not generate insights.")

                    # Extract only the actionable advice from the summary
                    # We can assume the actionable advice starts after certain keywords
                    actionable_advice_start = full_summary.lower().find('here are some suggestions')

                    if actionable_advice_start != -1:
                        ai_insights = full_summary[actionable_advice_start:]  # Extract only the actionable part
                    else:
                        ai_insights = full_summary  # If no specific advice found, use the whole text

                    return jsonify({'summary': ai_insights})

                else:
                    return jsonify({'summary': "Unexpected response format."})

            return jsonify({'summary': 'Failed to fetch insights from the model.'})

        except Exception as e:
            print(f"Error calling the Hugging Face API: {str(e)}")
            return jsonify({'summary': f'Error processing the request: {str(e)}'})

    return jsonify({'summary': 'No notes to summarize.'})


if __name__ == '__main__':
    app.run(debug=True)
