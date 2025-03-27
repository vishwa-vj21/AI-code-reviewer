import re

def analyze_code(code):
    suggestions = []

    # ✅ Detecting bad loops
    if "for " in code and "range" in code and "print(" in code:
        suggestions.append("Consider using a generator instead of a for loop.")

    # ✅ Detecting bad function names
    if re.search(r"\bdef [A-Z]", code):
        suggestions.append("Function names should be lowercase (PEP-8).")

    # ✅ Detecting unused imports
    unused_imports = re.findall(r"import (\w+)", code)
    if len(unused_imports) > 2:
        suggestions.append("Too many imports. Remove unused ones.")

    return suggestions
