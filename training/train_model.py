from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Define the absolute path for the models folder inside ai code reviewer/api/models
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
models_dir = os.path.join(base_dir, "..", "api", "models")  # Go up to project root, then into api/models

# Ensure the models directory exists
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

# Save the trained model and vectorizer inside api/models/
joblib.dump(model, os.path.join(models_dir, "model.pkl"))
joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))

print(f"✅ Model trained and saved in '{models_dir}/model.pkl'")
