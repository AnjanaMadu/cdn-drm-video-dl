sudo docker rm -f drmtgbot
sudo docker rmi drmtgbot_img

sudo docker build -t drmtgbot_img .
sudo docker run -d --name drmtgbot --restart=always drmtgbot_img