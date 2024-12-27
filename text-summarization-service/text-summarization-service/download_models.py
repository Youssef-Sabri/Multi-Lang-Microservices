from transformers import pipeline

def download_models():
    # List of models to preload
    models = [
        "facebook/bart-large-cnn",  # Default/informal model
        "t5-base",  # Formal model
        "google/pegasus-xsum"  # Technical model
    ]

    for model in models:
        print(f"Downloading model: {model}")
        pipeline("summarization", model=model)  # This downloads and caches the model

if __name__ == "__main__":
    download_models()
