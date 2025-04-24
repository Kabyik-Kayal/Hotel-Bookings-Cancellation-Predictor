# Hotel Booking Cancellations Predictor

# Data Ingestion

Retrieve Data from Google Cloud Storage Bucket


# Docker_Build (Ubuntu/Linux)

sudo docker run -d \
  --name jenkins-dind \
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind

# Setup Jenkins

1. Get Jenkins Access Password by running :

```bash
sudo docker logs jenkins-dind

```

2. Open https://localhost:8080 and login to Jenkins after installing suggested plugins

3. Setup Jenkins Container

```bash
sudo docker exec -u root -it jenkins-dind bash

apt update -y
apt install -y python3
python3 --version
ln -s /usr/bin/python3 /usr/bin/python
python --version
apt install -y python3-pip
apt install -y python3-venv
exit

sudo docker restart jenkins-dind

```
4. Jenkins Setup
