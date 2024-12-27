from flask import Flask, request, jsonify
import uuid
from models.summarizer import Summarizer

app = Flask(__name__)
summarizer = Summarizer()
tasks = {}

@app.route("/summarize", methods=["POST"])
def summarize():
    # Generate a unique ID for the request
    task_id = str(uuid.uuid4())
    
    # Store the initial status as 'In Progress'
    tasks[task_id] = {"status": "In Progress"}

    # Get input text and style from request
    data = request.json
    text = data.get("text", "")
    style = data.get("style", None)

    # Check if text is provided
    if not text:
        tasks[task_id]["status"] = "Failed"
        return jsonify({"error": "No text provided"}), 400

    try:
        # Perform summarization
        summary = summarizer.summarize(text, style)
        
        # Update status to 'Completed' and store the summary
        tasks[task_id]["status"] = "Completed"
        tasks[task_id]["summary"] = summary
        
        # Return task ID and the summary directly
        return jsonify({
            "task_id": task_id,
            "summary": summary
        }), 202
    except Exception as e:
        # Update status to 'Failed' in case of an error
        tasks[task_id]["status"] = "Failed"
        return jsonify({"error": str(e)}), 500

@app.route("/summarize/status/<task_id>", methods=["GET"])
def get_status(task_id):
    # Retrieve the status of the request
    task = tasks.get(task_id)
    if not task:
        # Return 404 if the task ID is not found
        return jsonify({"error": "Task not found"}), 404
    
    # Only return task_id and status (without the summary)
    return jsonify({
        "task_id": task_id,
        "status": task["status"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
