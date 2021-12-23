from azureml.core import  Webservice, Workspace, Model
from azureml.core import Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice
from dotenv import load_dotenv
import urllib.request
import os
import json
import requests


# ------- ENVIRONMENT VARIABLES --------
load_dotenv()
SUBSCRIPTION_ID = os.environ.get('SUBSCRIPTION_ID')
RESOURCE_GROUP = os.environ.get('RESOURCE_GROUP')
MLWORKSPACE = os.environ.get('MLWORKSPACE')


#Intializing AzureMLWorkspace
ws = Workspace(subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=MLWORKSPACE)

#Download model
# urllib.request.urlretrieve("https://aka.ms/bidaf-9-model", "model.onnx")
#Registering the model in AzureMLWorkspace
model = Model.register(ws, model_name="bidaf_onnx", model_path="./model.onnx")

##############################
# ----- LOCAL DEPLOYMENT -----
##############################
'''
env = Environment(name="project_environment")
dummy_inference_config= InferenceConfig(
    environment=env,
    source_directory='./source_dir',
    entry_script='./echo_score.py'
)

deployment_config = LocalWebservice.deploy_configuration(port=6789)

service = Model.deploy(
    ws,
    "myservice", 
    [model],
    dummy_inference_config,
    deployment_config, 
    overwrite=True
)
service.wait_for_deployment(show_output=True)

print(service.get_logs())

uri = service.scoring_uri
requests.get("http://localhost:6789")
headers = {"Content-Type": "application/json"}
data = {
    "query":"What color is the fox",
    "context": "The quick brown fox jumps over the lazy dog"
}
data = json.dumps(data)
response = requests.post(uri, data=data, headers=headers)
print(response.json())
'''

###################################
# ----- DEPLOYMENT TO AZUREML -----
###################################

env = Environment(name='myenv')
python_packages = ['nltk', 'numpy', 'onnxruntime']
for package in python_packages:
    env.python.conda_dependencies.add_pip_package(package)

inference_config = InferenceConfig(environment=env, source_directory='./source_dir', entry_script='./score.py')

deployment_config = AciWebservice.deploy_configuration(
    cpu_cores=0.5, memory_gb=1, auth_enabled=True
)
service = Model.deploy(
    ws,
    "myservice",
    [model],
    inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)

print(service.get_logs())

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

print(service.get_logs())
