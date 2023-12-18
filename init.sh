#! /bin/sh
sudo su
sudo yum update -y
sudo yum install git -y

# Pull from Git
wget https://github.com/MadsLang/annotation_setup.git
cd annotation_setup

# Get secrets
export ARGILLA_OWNER_API_KEY=$(aws ssm get-parameter --name ARGILLA_OWNER_API_KEY --query 'Parameter.Value' --output text)
export ARGILLA_OWNER_PASSWORD=$(aws ssm get-parameter --name ARGILLA_OWNER_PASSWORD --query 'Parameter.Value' --output text)

# install docker + docker-compose
sudo yum install docker -y
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo service docker start
sudo groupadd docker
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
wget -O docker-compose.yaml https://raw.githubusercontent.com/argilla-io/argilla/main/docker/docker-compose.yaml
sudo chmod -v +x /usr/local/bin/docker-compose
sudo chmod 666 /var/run/docker.sock
docker-compose up -d
