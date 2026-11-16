import json
import os
import boto3

lambda_client = boto3.client("lambda")
WORKER_FUNCTION_NAME = os.environ.get("WORKER_FUNCTION_NAME", "worker_lambda")


def lambda_handler(event, context):
  query_params = event.get("queryStringParameters") or {}

  try:
    a = int(query_params.get("a"))
    b = int(query_params.get("b"))
  except (TypeError, ValueError):
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {"error": "Parameters 'a' and 'b' must be valid integers."}
        ),
    }

  # Invoke the private microservice directly via AWS internal network
  response = lambda_client.invoke(
      FunctionName=WORKER_FUNCTION_NAME,
      InvocationType="RequestResponse",
      Payload=json.dumps({"a": a, "b": b}),
  )

  # Parse the response from the private worker
  worker_payload = json.loads(response["Payload"].read().decode("utf-8"))

  return {
      "statusCode": 200,
      "headers": {"Content-Type": "application/json"},
      "body": json.dumps({
          "a": a,
          "b": b,
          "result": worker_payload["result"],
          "iterations": worker_payload["iterations"],
          "source": "private-lambda-microservice",
      }),
  }
