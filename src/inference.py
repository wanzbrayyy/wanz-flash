from transformers import pipeline
import config

class CodeGenerator:
    def __init__(self):
        self.model_path = config.MODEL_OUTPUT_DIR
        print(f"Loading model from {self.model_path}...")
        try:
            self.generator = pipeline(
                'text-generation', 
                model=self.model_path, 
                tokenizer=self.model_path
            )
        except Exception as e:
            print(f"Error loading model: {e}. Did you train it first?")
            self.generator = None

    def generate(self, prompt, max_length=200):
        if not self.generator:
            return "Model not loaded."
        
        print(f"Generating code for: '{prompt}'...")
        result = self.generator(
            prompt, 
            max_length=max_length, 
            num_return_sequences=1,
            pad_token_id=50256
        )
        return result[0]['generated_text']