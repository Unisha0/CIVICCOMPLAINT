from pathlib import Path
import torch
import logging
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline,
)

# ===============================
# 🔧 LOGGING CONFIG
# ===============================
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ===============================
# 📁 PATH CONFIG
# ===============================
BACKEND_DIR = Path(__file__).resolve().parents[1]
ML_DIR = BACKEND_DIR / "ml_models"

CIVIC_MODEL = (ML_DIR / "civicconnect" / "best_model").resolve()
NEPALI_MODEL = (ML_DIR / "nepali" / "best_model").resolve()

# ===============================
# 🏛️ CATEGORY → AUTHORITY MAP
# ===============================
CATEGORY_AUTHORITY_MAP = {
    "water": "Water Authority",
    "electricity": "Electricity Authority",
    "road": "Road Authority",
    "garbage": "Garbage Authority",
}

# ✅ Allowed categories (STRICT CONTROL)
VALID_CATEGORIES = ["water", "electricity", "road", "garbage"]

# 🎯 Confidence threshold
CONFIDENCE_THRESHOLD = 0.70


# ===============================
# 🤖 CLASSIFIER CLASS
# ===============================
class ComplaintClassifier:
    def __init__(self):
        self.pipes = {}
        self.labels_cache = {}

    # ===============================
    # 📄 LOAD LABELS
    # ===============================
    def _load_labels(self, model_dir: Path):
        labels_file = model_dir / "labels.txt"
        if not labels_file.exists():
            raise FileNotFoundError(f"Missing labels file: {labels_file}")

        with open(labels_file, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]

    # ===============================
    # ✅ VALIDATE MODEL FILES
    # ===============================
    def _validate_model_dir(self, model_dir: Path):
        required_files = [
            "config.json",
            "model.safetensors",
            "tokenizer.json",
            "tokenizer_config.json",
            "labels.txt",
        ]

        if not model_dir.exists():
            raise FileNotFoundError(f"Model directory does not exist: {model_dir}")

        if not model_dir.is_dir():
            raise FileNotFoundError(f"Model path is not a directory: {model_dir}")

        missing = [name for name in required_files if not (model_dir / name).exists()]
        if missing:
            raise FileNotFoundError(
                f"Model directory is incomplete: {model_dir}. Missing: {', '.join(missing)}"
            )

    # ===============================
    # 🚀 LOAD MODEL PIPELINE
    # ===============================
    def _load_pipeline(self, model_dir: Path):
        model_dir = model_dir.resolve()

        # Cache for performance
        if model_dir in self.pipes:
            return self.pipes[model_dir], self.labels_cache[model_dir]

        self._validate_model_dir(model_dir)
        logger.info(f"Loading model from: {model_dir}")

        try:
            tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_dir,
                local_files_only=True,
                torch_dtype=torch.float32,
            )
        except Exception as e:
            logger.exception("Model loading failed")
            raise ValueError(f"Model loading error: {e}") from e

        pipe = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            top_k=1,
            device=0 if torch.cuda.is_available() else -1,
        )

        labels = self._load_labels(model_dir)

        self.pipes[model_dir] = pipe
        self.labels_cache[model_dir] = labels

        logger.info(f"Model loaded successfully from {model_dir}")
        return pipe, labels

    # ===============================
    # 🌐 LANGUAGE DETECTION
    # ===============================
    def detect_language(self, text: str):
        for ch in text:
            if "\u0900" <= ch <= "\u097F":
                return "ne"  # Nepali
        return "en"

    # ===============================
    # 🔮 PREDICT FUNCTION (CORE)
    # ===============================
    def predict(self, text: str):
        if not text or not text.strip():
            raise ValueError("Empty complaint text")

        text = text.strip()

        # Detect language
        lang = self.detect_language(text)

        # Select model
        model_dir = NEPALI_MODEL if lang == "ne" else CIVIC_MODEL

        # Load pipeline
        pipe, labels = self._load_pipeline(model_dir)

        # Run prediction
        result = pipe(text)[0]

        if isinstance(result, list):
            result = result[0]

        raw_label = result["label"]
        confidence = float(result["score"])

        # ===============================
        # 🔥 NORMALIZE CATEGORY
        # ===============================
        if raw_label.startswith("LABEL_"):
            idx = int(raw_label.split("_")[1])
            category = labels[idx]
        else:
            category = raw_label

        category = category.strip().lower()

        # ===============================
        # 🔒 VALIDATE CATEGORY
        # ===============================
        if category not in VALID_CATEGORIES:
            category = "unknown"

        # ===============================
        # 🏛️ MAP AUTHORITY
        # ===============================
        authority = CATEGORY_AUTHORITY_MAP.get(category)

        if not authority:
            authority = "General Authority"

        # ===============================
        # 🎯 CONFIDENCE STATUS
        # ===============================
        status = "CONFIDENT" if confidence >= CONFIDENCE_THRESHOLD else "UNCERTAIN"

        # ===============================
        # 📦 FINAL OUTPUT
        # ===============================
        return {
            "category": category,
            "confidence": confidence,
            "status": status,
            "authority": authority,
            "language": lang,
        }


# ===============================
# ♻️ SINGLETON INSTANCE
# ===============================
classifier_instance = None


def get_classifier():
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = ComplaintClassifier()
    return classifier_instance


# ===============================
# 🚀 PUBLIC FUNCTION
# ===============================
def classify_complaint(text: str):
    classifier = get_classifier()
    return classifier.predict(text)