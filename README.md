# What did I do?

This repository was used to practice and learn Azure ML deploying from the Azure ML SDK. 
Deploy.py containsa local deployment and a remote deployment. 
The remote deployment automatically generates the model and endpoint + compute in MLstudio, plus an image for the environment settings in Azure Container registry. 
</br>
</br>
## What to find in the files?
The request.py and request2.py both contain methods for communicating with the endpoint. However, I think the second method is better, because the first method requires azoreml.core to be installed in the environment, which is a bit of an overkill. 

## Model used for practicing?
Bidaf-9. Downloaded from here: https://aka.ms/bidaf-9-model 
For more information on what the bidaf-9 model ooes, please refer to:https://towardsdatascience.com/the-definitive-guide-to-bi-directional-attention-flow-d0e96e9e666b?gi=dc16cc30e093


## Guides used

Installing azureml-core: https://docs.microsoft.com/en-us/python/api/overview/azure/ml/install?view=azure-ml-py </br>
Tutorial: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=azcli 