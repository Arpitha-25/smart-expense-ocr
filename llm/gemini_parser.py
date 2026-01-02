from google import genai
import json
import time

def extract_receipt_data(image, ocr_text, api_key):
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert in extracting information from receipts.
    Extract:
    - company_name
    - date
    - total
    - items (description, quantity, price, total_price)

    Use null if missing.
    Return ONLY valid JSON.

    OCR Text:
    {ocr_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, {"text": prompt}]
    )

    cleaned = response.text.replace("```json", "").replace("```", "")
    return json.loads(cleaned)