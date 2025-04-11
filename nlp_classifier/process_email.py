from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load a lightweight semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Predefined categories and sample complaint texts
category_examples = {
    "Water": [
        "no water supply", "dry taps", "no water since morning", "low water pressure"
    ],
    "Electricity": [
        "no power", "power cut", "electricity not working", "lights gone"
    ],
    "Garbage": [
        "garbage not collected", "trash piling up", "overflowing bins", "bad smell from trash"
    ],
    "Road": [
        "potholes", "broken road", "uneven street", "damaged roads"
    ],
    "Sanitation": [
        "open sewage", "dirty drain", "water overflowing from drainage", "unhygienic area"
    ],
    "Stray Dogs": [
        "stray dog menace", "dogs attacking kids", "too many stray dogs"
    ]
}

# Flatten category samples for embedding
category_sentences = []
category_labels = []
for cat, phrases in category_examples.items():
    for phrase in phrases:
        category_sentences.append(phrase)
        category_labels.append(cat)

category_embeddings = model.encode(category_sentences, convert_to_tensor=True)

# Known constituency names
constituencies = [
    "Yelahanka", "Byatarayanapura", "Yeshwanthapura", "Dasarahalli", "Mahalakshmi Layout",
    "Malleshwaram", "Hebbal", "Pulakeshinagar", "Sarvagnanagar", "C.V. Raman Nagar",
    "Shivajinagar", "Shanti Nagar", "Gandhi Nagar", "Rajaji Nagar", "Govindraj Nagar",
    "Vijayanagar", "Chamarajpet", "Chickpet", "Basavanagudi", "Padmanabhanagar",
    "B.T.M. Layout", "Jayanagar", "Bommanahalli", "Bangalore South", "Mahadevapura",
    "Krishnarajapuram", "Anekal", "Bangalore Rural"
]

def process_email(subject, body):
    text = f"{subject} {body}".lower()

 
    email_embedding = model.encode(text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(email_embedding, category_embeddings)[0].cpu().numpy()

    best_idx = int(np.argmax(cosine_scores))
    predicted_category = category_labels[best_idx]
    confidence = round(float(cosine_scores[best_idx]), 2)

    detected_constituency = "Unknown"
    for name in constituencies:
        if name.lower() in text:
            detected_constituency = name
            break

    
    departments = {
        "Water": "BWSSB",
        "Electricity": "BESCOM",
        "Garbage": "BBMP - Waste",
        "Road": "BBMP - Roads",
        "Sanitation": "BBMP - Sanitation",
        "Stray Dogs": "BBMP - Animal Control"
    }
    department = departments.get(predicted_category, "Unassigned")

    return {
        "category": predicted_category,
        "constituency": detected_constituency,
        "department": department,
        "confidence": confidence
    }
