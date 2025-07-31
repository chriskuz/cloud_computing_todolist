# Unofficial README

# Requirements
- Flask
- Google Cloud
- sqlite3
- requests


# Author notes
- developed locally the front end and back end api
- created a new instance on google compute engine for the backend
- downloaded kubelet engine
- made a dockerfile and pushed to dockerhub (Dockerfile, YAML, requirements.txt, .dockerignore)
- created Google Cloud cluster


# Deploying Locally

To deploy this application locally, you must open two unique 


# Cloud Environment

- make sure you are using a Linux based OS (preferably a Ubuntu v24+)
- make sure apt is installed (needed for Docker and pip to work appropriately)
- make sure pip is installed (nneded for Docker to work appropriately)
- 

# Known Issues

1) Using a `/` as part of the todo item description will currently break the system. This is due to a `/` marker affecting how `sqlite3` 