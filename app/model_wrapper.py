# app/model_wrapper.py

USE_LLM = False
MODEL_NAME = "gpt4all-lora-quantized"

class LocalLLM:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.model = None

        if USE_LLM:
            try:
                from gpt4all import GPT4All
                self.model = GPT4All(model_name)
            except Exception as e:
                print("LLM load failed:", e)
                self.model = None

    def generate(self, prompt: str, max_tokens: int = 256):
        if not USE_LLM or self.model is None:
            return None
        try:
            return self.model.generate(prompt, max_tokens=max_tokens)
        except Exception as e:
            print("LLM error:", e)
            return None


llm = LocalLLM()