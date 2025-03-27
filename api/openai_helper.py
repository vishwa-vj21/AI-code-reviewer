import openai

# Replace with your actual OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key_here"

def openai_suggestions(code):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI code reviewer."},
                {"role": "user", "content": f"Analyze this code and suggest improvements:\n{code}"}
            ],
            api_key=OPENAI_API_KEY
        )
        return [response["choices"][0]["message"]["content"]]
    except Exception as e:
        return ["⚠️ OpenAI API Error: " + str(e)]
