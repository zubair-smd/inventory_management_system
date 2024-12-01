
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/inventory_management_system/nginx/nginx.conf /etc/nginx/sites-available/inventory_management
sudo ln -s /etc/nginx/sites-available/inventory_management /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/inventory_management /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

