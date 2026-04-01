# Civic Complaint Classification System Using DistilBERT

> A multilingual AI-powered civic complaint management system that automatically categorizes citizen complaints in **English and Nepali** using fine-tuned DistilBERT models.

![Research Poster]

*Published in Journal of Himalaya College of Engineering, Vol. X, Issue X — March 2026*  
*Authors: Ashmita Thapa, Jeevika Subedi, Nayana Bhatta, Unisha Chaulagain, Er. Nawaraj Singh Thakuri*  
*Department of Electronics and Computer Engineering, Himalaya College of Engineering, Tribhuvan University (TU), Lalitpur, Nepal*

---

## Overview

Manual complaint routing in public services leads to delays and misrouting. This system addresses that by automatically classifying citizen-submitted text complaints into predefined categories, routing them to the relevant authorities in real time.

**Complaint Categories:**
- Road
- Water
- Electricity
- Sanitation / Garbage

**Key Highlights:**
- Supports both **English** and **Nepali** language inputs
- English model achieves **~99.8% accuracy** on validation data
- Nepali model delivers strong performance despite limited training data
- Integrated with a Django REST API backend and Flutter mobile app

---

## Project Structure

```
.
├── backend/                        # Django REST API backend
│   └── mysite/
│       ├── accounts/               # User authentication
│       ├── authority/              # Authority/admin management
│       ├── citizen/                # Citizen profile & complaint submission
│       ├── complaint/              # Complaint handling & ML inference
│       └── ml_models/              # Trained DistilBERT model directories
│           ├── civicconnect/       # English complaint classifier
│           └── nepali/             # Nepali complaint classifier
│
├── civiccomplaints/                # Flutter mobile application
│   └── lib/
│       ├── screens/                # App screens (login, home, submit, etc.)
│       ├── services/               # API service calls
│       ├── widgets/                # Reusable UI components
│       └── theme/                  # App theme
│
├── project/                        # ML training & evaluation scripts
│   ├── civicconnect/               # English model pipeline
│   │   ├── train_distilbert.py
│   │   ├── predict_distilbert.py
│   │   └── evaluate_hard_test.py
│   └── nepali/                     # Nepali model pipeline
│       ├── train_distilbert.py
│       ├── predict_distilbert.py
│       └── generate_complaints.py
│
└── assets/                         # Repository assets (poster, images)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile App | Flutter 3.x (Dart) |
| Backend API | Django 6.0 (Python) |
| ML Models | DistilBERT (HuggingFace Transformers) |
| Database | SQLite (dev) |
| Tunneling (dev) | ngrok |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Flutter SDK 3.x
- pip

### Backend Setup

```bash
cd backend/mysite
pip install -r requirements.txt    # install Django & ML dependencies
python manage.py migrate
python manage.py runserver
```

> **Note:** Model weight files (`.safetensors`) are not included in this repository due to size limits. Place the trained model files at:
> - `backend/mysite/ml_models/civicconnect/best_model/model.safetensors`
> - `backend/mysite/ml_models/nepali/best_model/model.safetensors`

### Flutter App Setup

```bash
cd civiccomplaints
flutter pub get
flutter run
```

Update the API base URL in `civiccomplaints/lib/services/` to match your backend address (or ngrok URL for local testing).

### Training the Models

```bash
cd project/civicconnect      # or project/nepali
pip install -r requirements.txt
python train_distilbert.py
```

---

## Model Performance

| Model | Accuracy | F1 (Weighted) |
|---|---|---|
| English (CivicConnect) | ~99.8% | ~0.998 |
| Nepali | High | Reliable across 4 classes |

Evaluation includes confusion matrices, precision/recall/F1 per class, and training/validation loss curves — see `project/civicconnect/results/` and `project/nepali/results/`.

---

## License

This project is for academic research purposes. See individual component directories for any additional license information.
