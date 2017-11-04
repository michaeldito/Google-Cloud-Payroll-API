# Please note that you would still need to update the internal ip address
# that are loadbalanced on 

# This can be done in 2 ways :

# Option 1 : 
#		alter the file "default" in your 
# 		home directory before running the script
#  		and than run this script after.
# 		(This step requires you to unzip the folder LoadBalancer.tar.gz)

# Option 2 :
# 		Run the script and directly alter the Nginx file 
# 		/etc/nginx/sites-available/default 


#uncompress my files
tar -xvzf LoadBalancer.tar.gz

# install nginx
sudo apt-get update
sudo apt-get install -y nginx


# copy the file I already altered to allow 4096 worker connections 
# like in our Lab 02 scaling
sudo cp ./LoadBalancer/nginx.conf /etc/nginx/nginx.conf


# make some neccessary nginx files/folders
sudo mkdir /etc/systemd/system/nginx.service.d
sudo bash -c 'echo -e "[Service]nLimitNOFILE=65536" > /etc/systemd/system/nginx.service.d/local.conf'
sudo systemctl daemon-reload
sudo systemctl restart nginx


# copy the default file to the apporipate Nginx folder
# this is the file with internal ip addresss load balanced on
sudo cp ./LoadBalancer/default /etc/nginx/sites-available/default


# reset the loadbalancer server
sudo service nginx reload


