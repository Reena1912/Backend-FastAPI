# Challenge 1: The Text Analyzer API

## Objective
Implement a `POST` endpoint at `/analyze` that takes a piece of text, performs some basic calculations, and returns structured statistics.

## Requirements

1. **Endpoint**: `POST /analyze`
2. **Input Payload** (JSON):
   ```json
   {
     "text": "Your string here"
   }
   ```
   *Hint: You'll need to define a Pydantic model for this input.*

3. **Output Payload** (JSON) on Success:
   ```json
   {
     "word_count": 3,
     "char_count": 13,
     "longest_word": "string",
     "is_palindrome": false
   }
   ```
   - `word_count`: Total number of words.
   - `char_count`: Total number of characters (excluding spaces).
   - `longest_word`: The longest word in the text.
   - `is_palindrome`: A boolean representing whether the text is a palindrome (reads the same backward as forward, ignoring casing and spaces).

4. **Validation & Errors**:
   - If the user sends an empty string `""` or only whitespace `"   "`, return an HTTP `400 Bad Request` status code with the detail: `"Text cannot be empty"`.

---

## How to Start

1. Open your code editor a
2. Open [main.py] or whatever your filename is
3. Import `BaseModel` from `pydantic` and `HTTPException` from `fastapi`:
   ```python
   from pydantic import BaseModel
   from fastapi import FastAPI, HTTPException
   ```
4. Define your request Pydantic model:
   ```python
   class TextRequest(BaseModel):
       text: str
   ```
5. Write the endpoint function:
   ```python
   @app.post("/analyze")
   async def analyze_text(request: TextRequest):
       # 1. Validate the text isn't empty
       # 2. Split the text into words and perform calculations
       # 3. Return the statistics dictionary
   ```

6. Save the file.
7. Run the server using:
   ```bash
    uvicorn Challenges.TextAnalyze.Text_analyze_api:app --reload --reload-dir Challenges
   ```

8. Go to `http://127.0.0.1:8000/docs` in your browser, click **Try it out** on your `/analyze` endpoint, enter test text, and see if it works!
