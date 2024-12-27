from transformers import pipeline

class Summarizer:
    def __init__(self, style_models=None):
        # Define models for different styles
        self.style_models = style_models or {
            'informal': 'facebook/bart-large-cnn',  # Default model for informal style
            'formal': 't5-base',  # Example formal model (you can replace with a more formal-specific model)
            'technical': 'google/pegasus-xsum'  # Example technical model
        }
        # Default model if no style is specified
        self.default_model = 'facebook/bart-large-cnn'
        # Cache for loaded pipelines
        self.pipelines = {}

    def _get_pipeline(self, style):
        """Retrieve or load the pipeline for the specified style."""
        model_name = self.style_models.get(style, self.default_model)
        if model_name not in self.pipelines:
            self.pipelines[model_name] = pipeline("summarization", model=model_name)
        return self.pipelines[model_name]

    def summarize(self, text, style=None):
        # Get the appropriate summarizer pipeline based on the requested style
        summarizer = self._get_pipeline(style)

        # Generate the summary
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

        return summary
