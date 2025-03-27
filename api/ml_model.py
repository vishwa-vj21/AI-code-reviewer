from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# ✅ Ensure models are saved inside `api/models/`
models_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(models_dir, exist_ok=True)

# Sample training dataset
X = [
    "for i in range(10): print(i)",  # Inefficient loop
    "def Hello(): return 5",  # Bad function name
    "import os\nimport sys\nimport random\nx = 5",  # Unused imports
    "if x == True: print('Yes')",  # Bad comparison (should use `if x:`)
    "def add(x, y) -> int:\n return x + y",  # Missing docstring
    "try:\n x = 10 / 0 \nexcept: print('Error')",  # Bare except block
    "class test:\n def __init__(self): pass",  # Class name not in PascalCase
    "print('Debugging')\n#TODO: Refactor this",  # Leftover debugging print statements
]

y = [
    "Consider using a generator instead of a for loop.",
    "Function names should be lowercase (PEP-8).",
    "Unused imports detected. Remove unused modules.",
    "Use `if x:` instead of `if x == True`.",
    "Add a docstring explaining the function.",
    "Avoid using bare `except:` blocks; catch specific exceptions.",
    "Class names should follow PascalCase.",
    "Remove debugging print statements and TODO comments before production.",
]

# Train the model
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vectorized, y)

# Save the trained model
joblib.dump(model, os.path.join(models_dir, "model.pkl"))
joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))

print(f"✅ Model trained and saved in '{models_dir}/model.pkl'")

# Function to suggest fixes
def suggest_fixes(code):
    model_path = os.path.join(models_dir, "model.pkl")
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return ["⚠️ Model files missing. Run `train_model.py` first."]

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    input_vector = vectorizer.transform([code])
    prediction = model.predict(input_vector)

    return [prediction[0]]
