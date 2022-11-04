sudo apt update -y

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
/etc/apt/sources.list.d/jenkins.list'

sudo apt update
sudo apt install jenkins

sudo systemctl daemon-reload
sudo systemctl start jenkins

sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl enable jenkins
sudo systemctl status jenkins