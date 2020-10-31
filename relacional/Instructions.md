# Deploy and Use MariaDB

Be sure you have docker install, running "docker --version".
If you don't have it, then do the following:
```bash
url -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
docker --version
```

Now, build image :
```bash
sudo docker build -t maria .
```

Then, run maria (change DB_PASSWORD on your will):
```bash
sudo docker run -e MYSQL_ROOT_PASSWORD=DB_PASSWORD maria
```
