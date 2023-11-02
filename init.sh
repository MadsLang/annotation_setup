#! /bin/sh
yum update -y
amazon-linux-extras install docker
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
service docker start
usermod -a -G docker ec2-user
chkconfig docker on
env ANNOTATOR_USERNAME="annotator"
env OWNER_PASSWORD="SmukSomEtSterneskud"
env ADMIN_PASSWORD="CostaDelSol"
env ANNOTATOR_PASSWORD="writelabels"
env LOAD_DATASETS="none"
env OWNER_API_KEY="0b2c3901-69b8-47a1-86bb-6b3eed4b1cb8"
env ADMIN_API_KEY="7c6e2021-e926-4083-aca5-4db0e49d9902"
wget -O docker-compose.yaml https://raw.githubusercontent.com/argilla-io/argilla/main/docker/docker-compose.yaml && docker-compose up -d
