from azureml.core import Webservice, Workspace
import requests
import json
import os
from dotenv import load_dotenv

# ------- ENVIRONMENT VARIABLES --------
load_dotenv()
SUBSCRIPTION_ID = os.environ.get('SUBSCRIPTION_ID')
RESOURCE_GROUP = os.environ.get('RESOURCE_GROUP')
MLWORKSPACE = os.environ.get('MLWORKSPACE')


#Intializing AzureMLWorkspace
ws = Workspace(subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=MLWORKSPACE)

service = Webservice(workspace=ws, name="myservice")
scoring_uri = service.scoring_uri

# If the service is authenticated, set the key or token
key, _ = service.get_keys()

# Set the appropriate headers
headers = {"Content-Type": "application/json"}
headers["Authorization"] = f"Bearer {key}"

# Make the request and display the response and logs
data = {
    "query": "What color is the fox",
    "context": "The quick brown fox jumped over the lazy dog.",
}

data = json.dumps(data)
resp = requests.post(scoring_uri, data=data, headers=headers)
print(resp.text)
