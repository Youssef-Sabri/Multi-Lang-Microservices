from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uuid

# Initialize FastAPI app
app = FastAPI()

# Initialize the Hugging Face translation pipeline
translator = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")

# In-memory store to track request statuses
translation_status = {}

# Request model for translation
class TranslationRequest(BaseModel):
    text: str

@app.post("/translate/en2ar")
def translate(request: TranslationRequest):
    # Generate a unique ID for the request
    request_id = str(uuid.uuid4())
    
    # Store the initial status as 'In Progress'
    translation_status[request_id] = "In Progress"

    try:
        # Perform translation
        result = translator(request.text)
        # Update status to 'Completed'
        translation_status[request_id] = "Completed"
        return {"id": request_id, "translated_text": result[0]["translation_text"]}
    except Exception as e:
        # Update status to 'Failed' in case of an error
        translation_status[request_id] = "Failed"
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/translate/en2ar/status/{id}")
def get_status(id: str):
    # Retrieve the status of the request
    status = translation_status.get(id)
    if status is None:
        # Return 404 if the ID is not found
        raise HTTPException(status_code=404, detail="Translation request not found")
    return {"id": id, "status": status}
