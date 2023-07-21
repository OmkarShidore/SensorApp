import os
import json
import awsgi
from src.routes import app

def lambda_handler(event, context=None):
    #Lambda handler
    print(f"{'-'*20}EVENT{'-'*20}")
    print(event)
    for key in os.environ:
        print(key, os.environ[key])
    print(f"{'-'*20}END ENVIRON{'-'*20}")
    response = awsgi.response(app, event, context)
    print(f"Response: {response}")
    return response

if __name__ == '__main__':
    if "LOCAL_RUN" in os.environ and os.environ["LOCAL_RUN"] == "True":
        with open("event.json") as json_file:
            event = json.load(json_file)
        lambda_handler(event)