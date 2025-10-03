class EnsembleModel:
    def __init__(self, model_a, model_b, combine="or"):
        self.model_a = model_a
        self.model_b = model_b
        self.combine = combine  

    def predict(self, x):
        try: 
            result_a = self.model_a.predict(x)
        except Exception as e:
            print(f"[ERROR] model_a failed on input, error: {e}")
            import traceback
            traceback.print_exc()
            result_a = 0  # fallback

        try:
            result_b =self.model_b.predict(x)
            
        except Exception as e:
            print(f"[ERROR] model_b failed on input, error: {e}")
            import traceback
            traceback.print_exc()
            result_b = 0  # fallback

        if self.combine == "or":
            return int(bool(result_a) or bool(result_b))
        elif self.combine == "and":
            return int(bool(result_a) and bool(result_b))
        elif self.combine == "avg":
            return (result_a + result_b) / 2
        else:
            raise ValueError(f"Unknown combine mode: {self.combine}")