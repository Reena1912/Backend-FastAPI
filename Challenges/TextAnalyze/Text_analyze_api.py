from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app= FastAPI()

class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "welcome home"}


@app.post("/analyze")
async def analyze_text(request: TextRequest):
        # 'request' now contains the user's input.
        # We can access the text string using: request.text
    user_text=request.text

    # Validation (Checking if it's empty)
    if not user_text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    
    # Count the words
    words= user_text.split()
    word_count= len(words)
    

    # Count characters (excluding spaces)
    no_spaces= user_text.replace(" ", "")
    char_count= len(no_spaces)

    #Find the longest word # Find the longest item in the 'words' list based on its length (key=len) 
    longest_word= max(words, key=len)
    

    # 6. Palindrome Check
    cleaned = user_text.lower().replace(" ", "")
    is_palindrome = cleaned == cleaned[::-1]
    

    return {
        "word_count": word_count,
        "char_count": char_count,
        "longest_word": longest_word,
        "is_palindrome": is_palindrome
    }
