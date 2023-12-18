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

1) Configure AWS CLI with your credentials.

2) Add secrets ARGILLA_OWNER_API_KEY and ARGILLA_OWNER_PASSWORD to AWS SSM with AWS CLI (Add your own password/apikeys):
```
aws ssm put-parameter \
    --name "ARGILLA_OWNER_PASSWORD" \
    --value "" \
    --type String \
    --overwrite
```

3) Deploy ressources with Terraform
```
terraform validate
terraform apply
```

Now, Argilla should be accessible from your public IP. To add data, set this env var to the IP of your instance:
```
export ARGILLA_SERVER_API_URL="http://localhost:6900"
```


## Run Argilla server locally

First set relevant env variables.

In a locally hosted setup with default values from argilla, just run
```
source .env
```
where you have set ARGILLA_OWNER_API_KEY, ARGILLA_OWNER_PASSWORD and ARGILLA_SERVER_API_URL.

Then simply run:
```
docker-compose up -d
```

## Create annotation project with users and dataset

If setup is deployed to the cloud, you should have defined the IPv4 instead of localhost and a secret api key for the default owner profile.

Then run:
```
poetry run python src/create_project.py --workspacename my-workspace --dataset dataset_v1
```

Remember that dataset_v1 should correspond to settings in `config/dataset.json`
