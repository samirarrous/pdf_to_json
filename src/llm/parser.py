import json
import re


def extract_json_block(text: str) -> str:
    """
    Tries to extract the first JSON block from a LLM response.
    """

    # 1. Remove Markdown code fences ```json and ```
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # 2. Try to extract a JSON object using regex
    match = re.search(r"\{.*\}", text, re.S)

    if match:
        return match.group()

    # If no JSON found, return raw text
    return text


def parse_json_safe(response: str, max_retry: int = 2):
    """
    Safely parses a LLM response into valid JSON.
    Includes retry mechanism with basic repair attempts.
    """

    for _ in range(max_retry + 1):
        try:
            # Clean and extract JSON block
            cleaned = extract_json_block(response)

            # Attempt to parse JSON
            return json.loads(cleaned)

        except json.JSONDecodeError:
            # If parsing fails, try to repair the JSON
            response = repair_json(response)

    # If all attempts fail, return structured error
    return {
        "error": "invalid_json",
        "raw_response": response
    }


def repair_json(text: str) -> str:
    """
    Applies heuristic fixes to common LLM JSON errors.
    """

    # Remove leading/trailing whitespace
    text = text.strip()

    # Extract only the JSON part if embedded in text
    match = re.search(r"\{.*\}", text, re.S)
    if match:
        text = match.group()

    # Fix single quotes to double quotes (common LLM mistake)
    text = text.replace("'", "\"")

    # Remove trailing commas in objects and arrays
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)

    return text 