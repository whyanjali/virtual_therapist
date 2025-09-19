from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai   # ✅ old style import works with openai==0.28
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()  # loads .env into environment

# Set your OpenAI key
openai.api_key = os.getenv("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")
# OR directly set it here:
# openai.api_key = "your_api_key_here"

class UserMessage(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Hello from virtual therapist"}

@app.post("/chat")
def chat(user_message: UserMessage):
    try:
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not set")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # ✅ works in 0.28
            messages=[
                {"role": "system", "content": "You are a helpful, empathetic virtual therapist."},
                {"role": "user", "content": user_message.message}
            ],
            temperature=0.7
        )

        reply = response["choices"][0]["message"]["content"]
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


