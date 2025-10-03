
import numpy as np
from .featureextractor import SafePEFeatureExtractor

class DummyModel(object):
    def __init__(self, model_path: str = "lgbm_model_0.txt", thresh: float = 0.5, name: str = "lightgbm"):
        import lightgbm as lgb
        self.model = lgb.Booster(model_file=model_path)
        self.thresh = thresh
        self.extractor = SafePEFeatureExtractor()
        self.__name__ = name

    def predict(self, bytez: bytes) -> int:
        # Extract features from raw PE file
        features = self.extractor.feature_vector(bytez)
        features = np.array(features).reshape(1, -1)

        # Predict probability of being malicious
        prob = self.model.predict(features)[0]
        return int(prob > self.thresh)

    def model_info(self):
        return {"thresh": self.thresh, "name": self.__name__}
