import os

from extractors.text_extractor import extract_text

from llm.client import call_llm
from llm.prompt import build_prompt
from llm.parser import parse_json_safe


def process_pdf(pdf_path: str, user_prompt: str, schema: str):
    # 1. EXTRACTION TEXTE
    poppler_path = os.getenv("POPPLER_PATH")
    text = extract_text(pdf_path, poppler_path=poppler_path)

    print("=== OCR RESULT ===")
    print(text)

    # 2. BUILD PROMPT
    prompt = build_prompt(user_prompt, schema, text)

    # 3. CALL LLM
    response = call_llm(prompt)

    # 4. PARSE + CLEAN JSON
    result = parse_json_safe(response)
    return result