# annotation_setup
Deployment of data labelling service (e.g. Argilla) on AWS


## Setup

```
poetry install
poetry run pre-commit install
```

+ install terraform cli

## Deploy base ressources on AWS

To deploy the Argilla instance, you need to deploy VPC, a public subnet, etc. to host the EC2-instance.

First, get temporary credentials from AWS. Then:
```
terraform validate
terraform apply
```

## Deploy EC2 with Argilla server and ElasticSearch backend

(TODO)

## Run Argilla server locally

```
docker-compose up -d
```

## Create annotation project with users and dataset

First set relevant env variables.

In a locally hosted setup with default values from argilla, just run
```
source .env
```

If setup is deployed to the cloud, you should have defined the IPv4 instead of localhost and a secret api key for the default owner profile.

Then run:
```
poetry run python src/create_project.py --workspacename my-workspace --dataset dataset_v1
```

Remember that dataset_v1 should correspond to settings in `config/dataset.json`
