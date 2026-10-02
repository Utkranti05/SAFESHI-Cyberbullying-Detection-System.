import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("dataset/cyberbullying_final_dataset_v3.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 2. INPUT AND OUTPUT
# --------------------------------------------------

X = df["text"].astype(str)
y = df["label"]


# --------------------------------------------------
# 3. TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 4. TF-IDF FEATURES
# --------------------------------------------------

features = FeatureUnion([
    (
        "word",
        TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=50000,
            sublinear_tf=True
        )
    ),
    (
        "char",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=30000,
            sublinear_tf=True
        )
    )
])


# --------------------------------------------------
# 5. TRANSFORM TEXT
# --------------------------------------------------

X_train_features = features.fit_transform(X_train)
X_test_features = features.transform(X_test)

print("\nFeatures created successfully!")


# --------------------------------------------------
# 6. TRAIN MODEL
# --------------------------------------------------

import numpy as np

class_counts = y_train.value_counts()
soft_weights = {
    label: float(np.sqrt(len(y_train) / (len(class_counts) * count)))
    for label, count in class_counts.items()
}

model = LogisticRegression(
    max_iter=2000,
    class_weight=soft_weights
)
print("\nTraining model...")

model.fit(X_train_features, y_train)

print("Training completed!")


# --------------------------------------------------
# 7. TEST MODEL
# --------------------------------------------------

y_pred = model.predict(X_test_features)

accuracy = accuracy_score(y_test, y_pred)

print("\n==========================================")
print("MODEL TEST RESULTS")
print("==========================================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 8. SAVE MODEL + FEATURES
# --------------------------------------------------

model_folder = Path("model")
model_folder.mkdir(exist_ok=True)

joblib.dump(
    {
        "features": features,
        "model": model
    },
    model_folder / "cyberbullying_model_v3.pkl"
)

print("\n==========================================")
print("MODEL SAVED SUCCESSFULLY!")
print("==========================================")

print("\nSaved as:")
print("model/cyberbullying_model_v3.pkl")