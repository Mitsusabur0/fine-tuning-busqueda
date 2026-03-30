import json

import boto3

import config


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
                {"role": "system", "content": "You are a helpful assistant."},
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


def main():
    prompt = "Example prompt"
    response_body = invoke_model(prompt)
    print(response_body)


if __name__ == "__main__":
    main()
