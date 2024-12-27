from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import uuid
import json

# Initialize Hugging Face summarizer
summarizer = pipeline("summarization")

# In-memory store for request statuses
summarization_status = {}

@csrf_exempt
def summarize(request):
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body)
            text = body.get("text", "")
            max_length = body.get("max_length", 130)
            min_length = body.get("min_length", 30)
            style = body.get("style", "default")  # Optional style parameter

            # Validate input
            if not text:
                return JsonResponse({"error": "Text is required"}, status=400)

            # Generate unique request ID
            request_id = str(uuid.uuid4())
            summarization_status[request_id] = "In Progress"

            # Perform summarization
            summary = summarizer(
                text, max_length=max_length, min_length=min_length, do_sample=False
            )[0]["summary_text"]

            # Customize style (optional)
            if style == "formal":
                summary = f"FORMAL STYLE: {summary}"
            elif style == "informal":
                summary = f"INFORMAL STYLE: {summary}"
            elif style == "technical":
                summary = f"TECHNICAL STYLE: {summary}"

            # Update status and return result
            summarization_status[request_id] = "Completed"
            return JsonResponse({"id": request_id, "summary": summary}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_status(request, id):
    if request.method == "GET":
        # Check if the request ID exists
        status = summarization_status.get(id)
        if not status:
            return JsonResponse({"error": "Request ID not found"}, status=404)
        return JsonResponse({"id": id, "status": status}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
