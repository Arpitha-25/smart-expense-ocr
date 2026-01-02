import streamlit as st
import os
from ocr.preprocess import preprocess_image
from ocr.extractor import load_image_for_llm
from llm.gemini_parser import extract_receipt_data
from storage.save import save_json
from dotenv import load_dotenv

load_dotenv()

API_KEY = (
    os.getenv("GOOGLE_API_KEY")
    or st.secrets["GOOGLE_API_KEY"]
)

API_KEY = st.secrets["GOOGLE_API_KEY"]

st.title("Smart OCR Expense Automation System")

uploaded = st.file_uploader("Upload Receipt", type=["jpg","png"])

if uploaded:
    os.makedirs("data/raw_images", exist_ok=True)
    image_path = f"data/raw_images/{uploaded.name}"

    with open(image_path, "wb") as f:
        f.write(uploaded.read())

    preprocess_image(image_path)
    image = load_image_for_llm(image_path)

    extracted = extract_receipt_data(
        image=image,
        ocr_text="",
        api_key=API_KEY
    )

    save_json(extracted, uploaded.name.replace(".jpg", ".json"))

    st.success("Receipt processed successfully!")
    st.json(extracted)