from thrember import PEFeatureExtractor
import numpy as np

class SafePEFeatureExtractor(PEFeatureExtractor):
    def raw_features(self, bytez):
        try:
            return super().raw_features(bytez) or {}
        except Exception as e:
            print(f"[DEBUG] raw_features failed: {e}")
            return {}

    def feature_vector(self, bytez):
        raw = self.raw_features(bytez)
        vectors = []

        for fe in self.features:
            if fe.name in raw and raw[fe.name] is not None:
                try:
                    vectors.append(fe.process_raw_features(raw[fe.name]))
                except Exception as e:
                    print(f"[DEBUG] Skipped feature {fe.name}: {e}")
            else:
                # skip missing or None features
                print(f"[DEBUG] Skipped missing feature {fe.name}")
                continue

        if not vectors:
            # return a zero vector if nothing usable
            return np.zeros(self.dim)

        return np.concatenate(vectors)
