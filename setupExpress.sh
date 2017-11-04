#uncompress the file myFirstExpressProject.tar.gz
tar -xvzf myFirstExpressProject.tar.gz

# install node
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs


# an instalation library that installs all neccessary files  to setup basic Express server
# -g is global install
sudo npm install -g express-generator


# install the ip library that allows us to get the internal ipaddress from within node.js app
# it should use "ip" : "~3.10.10"
sudo npm install -g ip


# **** old code **** 
# if you want to set up your own skelton project instead of using mine
# run the command below  to create an Express project

# express yourFirstExpressServerFolderName


# install hogan styling libraries, -c allows css style sheets, less is a specific package of css libraries
# these templates use the Mustache templating library developed by Twitter
# this library allows us to create html/javascript views of file type ".hjs" similar to ".ejs" in cs355

# --hogan is supposbly twitters version of Mustache
# less is a specific version or flavor, there is one other flavor called stylus

# express myFirstExpressProject --hogan -c less
# **** End old code **** 

# looks at your package.json file and tries to install the dependencies needed 
# to create the node.js server
cd myFirstExpressProject && npm install


# ------------------- Code to run Server beloe --------------------
# there are 2 ways to run the server

# ********* Optional 1 install nodemon  ***********
# nodemon is a node application that watches your project files for changes and is supposed to
# automatically restart the server when files are saved
sudo npm install -g nodemon


sudo nodemon bin/www #<-- runs the server on port 80 
# ***************** End of optinal program *************

# ++++++++++++ OR ++++++++++

# *************** Option 2 use the below command ************
# DEBUG is a flag that allows you to use node.js debugger to debug your server
# DEBUG takes the FolderName of your project as parameter 

# command below to manually run the 
# DEBUG=myfirstexpressproject:* npm start
# ***************  End option 2 *****************

# to test the server there are 2 options:

# option 1 use a web browser and the url
# If you get an error it could be b/c you are using https instead of http in the url 
#		 http://your_external_ipadress/

# 	example : http://35.190.150.93/ 

# option 2 use curl in terminal
# 		curl http://your_external_ipadress/

# example : curl http://35.190.150.93/ 







