import csv
import json
import os
import re
import boto3
import config
from system_prompt.generation_sys_prompt import sys_prompt


input_file = os.getenv("INPUT_FILE", "inputs/full/user_inputs.csv")
output_file = os.getenv("OUTPUT_FILE", "outputs/full/training_set.csv")



JSON_RESPONSE_PATTERN = re.compile(
    r"<json_response>\s*(.*?)\s*</json_response>",
    re.DOTALL,
)
REASONING_PATTERN = re.compile(
    r"<reasoning>.*?</reasoning>",
    re.DOTALL,
)


def get_bedrock_client():
    session = boto3.Session(profile_name=config.AWS_PROFILE_LLM)
    return session.client(
        service_name="bedrock-runtime",
        region_name=config.AWS_REGION,
    )


def invoke_model(prompt):
    client = get_bedrock_client()

    body = json.dumps(
        {
            "messages": [
                {"role": "system", "content": f"{sys_prompt}"},
                {"role": "user", "content": prompt},
            ],
            "temperature": config.TEMPERATURE,
            "max_tokens": 4000,
        }
    )

    response = client.invoke_model(
        modelId=config.MODEL_ID,
        body=body,
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    return response_body


def extract_text_from_response(response_body):
    if isinstance(response_body, str):
        return response_body

    if isinstance(response_body, list):
        parts = [extract_text_from_response(item) for item in response_body]
        return "\n".join(part for part in parts if part)

    if not isinstance(response_body, dict):
        return ""

    for key in ("output_text", "generation", "text", "content"):
        if key in response_body:
            extracted = extract_text_from_response(response_body[key])
            if extracted:
                return extracted

    if "output" in response_body:
        message = response_body["output"].get("message", {})
        extracted = extract_text_from_response(message)
        if extracted:
            return extracted

    if "message" in response_body:
        extracted = extract_text_from_response(response_body["message"])
        if extracted:
            return extracted

    if "messages" in response_body:
        extracted = extract_text_from_response(response_body["messages"])
        if extracted:
            return extracted

    if "choices" in response_body:
        extracted = extract_text_from_response(response_body["choices"])
        if extracted:
            return extracted

    if response_body.get("type") == "text" and "text" in response_body:
        return response_body["text"]

    if "content" in response_body and isinstance(response_body["content"], list):
        parts = []
        for item in response_body["content"]:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            else:
                nested = extract_text_from_response(item)
                if nested:
                    parts.append(nested)
        return "\n".join(part for part in parts if part)

    collected_parts = []
    for value in response_body.values():
        extracted = extract_text_from_response(value)
        if extracted:
            collected_parts.append(extracted)

    return "\n".join(collected_parts)


def extract_json_tag_content(response_text):
    cleaned_response = REASONING_PATTERN.sub("", response_text or "")
    match = JSON_RESPONSE_PATTERN.search(cleaned_response)
    if not match:
        return None
    return match.group(1).strip()


def read_input_rows(csv_path):
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)

        if not reader.fieldnames or reader.fieldnames != ["user_input"]:
            raise ValueError(
                f"Expected exactly one column named 'user_input' in {csv_path}."
            )

        return list(reader)


def get_completed_row_count(csv_path):
    if not os.path.exists(csv_path):
        return 0

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as outfile:
        reader = csv.reader(outfile)
        rows = list(reader)

    if not rows:
        return 0

    header = rows[0]
    if header != ["user_input", "filters_json"]:
        raise ValueError(
            f"Unexpected header in output file {csv_path}. "
            "Expected ['user_input', 'filters_json']."
        )

    return max(len(rows) - 1, 0)


def ensure_output_file(csv_path):
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)

    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        return

    with open(csv_path, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["user_input", "filters_json"])


def append_output_row(csv_path, user_input, filters_json):
    with open(csv_path, "a", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([user_input, filters_json])
        outfile.flush()


def process_row(user_input):
    try:
        response_body = invoke_model(user_input)
        response_text = extract_text_from_response(response_body)
        extracted_json = extract_json_tag_content(response_text)
        if extracted_json is None:
            return "failed", False
        return extracted_json, True
    except Exception:
        return "failed", False


def main():
    input_rows = read_input_rows(input_file)
    total_lines = len(input_rows)

    ensure_output_file(output_file)
    completed_rows = get_completed_row_count(output_file)

    if completed_rows > total_lines:
        raise ValueError(
            f"Output file already has {completed_rows} completed rows, "
            f"but input only has {total_lines} rows."
        )

    if completed_rows == total_lines:
        print(f"No pending rows. {completed_rows}/{total_lines} already completed.")
        return

    for row_index in range(completed_rows, total_lines):
        user_input = input_rows[row_index]["user_input"]
        filters_json, is_success = process_row(user_input)
        append_output_row(output_file, user_input, filters_json)

        status = "SUCCESS" if is_success else "FAILED"
        print(f"[{row_index + 1}/{total_lines}] {status}")


if __name__ == "__main__":
    main()
