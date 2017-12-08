# A RESTful Auto-Scaling Payroll API

A scalable REST API to calculate your payroll, using Flask, Google Cloud, and Pub/Sub.
Two scripts are provided for each component, one will use Google SQL, the other will
use Google Cloud Spanner.

## Setup
In order to use Pub/Sub, a service account key with Pub/Sub access should be set up.

## Google Cloud SQL
If you opt for Cloud SQL as your database, you must install the cloud sql proxy.
https://cloud.google.com/sql/docs/mysql/sql-proxy

## Google Cloud Spanner
If you opt for Cloud Spanner as your database, go ahead and create the instance.
https://cloud.google.com/spanner/docs/create-manage-instances

Now use spanner.sql to create your tables.

## Base Image
The easiest way to set up Application, Accruals, Delivery, and Translator is to create
a base image with all libraries needed. Install all requirements with:
`pip install -r requirements`
Now, go ahead and create your base image (make sure it contains the sql-proxy if you
are using Cloud SQL).

## Instance Template
In order to Load Balancer you need a Managed Instance Group. To create a Managed Instance
Group, you need an Instance Template.

## Managed Instance Group
Now, create your Managed Instance Group using your Instance Template.
https://cloud.google.com/compute/docs/instance-groups/distributing-instances-with-regional-instance-groups

## Load Balancer
You are now ready to enable the Load Balancer.   
https://cloud.google.com/compute/docs/load-balancing/network/

## Auto-Scaling
Now that the Load Balancer is enabled, you can opt to turn on Auto-Scaling.
https://cloud.google.com/compute/docs/autoscaler/scaling-cpu-load-balancing

**The service should now be ready.**

## Startup Scripts
Each component has a startup script, here are their locations:

Application - `restserver/start-server.sh`

The following components have 2 options: one script is for the SQL database, the other is for Spanner.
			SQL				Spanner  
Accruals    - `accruals/accruals.py` 		`accruals/accruals_spanner.py`     
Delivery    - `delivery/delivery.py`		`delivery/delivery_spanner.py`     
Translator  - `translator/translator.py`  	`translator/translator_spanner.py`   

## Testing
Use test.py to test your application. Be sure to update the IP address with your Load Balancer's IP.
The test.py script requires one argument, and has a second optional argument if you'd like to test
your services auto-scaling.

Examples:   
`python test.py createCompany`  
`python test.py addEmployee`  
`python test.py submit`   
`python test.py calculateAccruals`   
`python test.py deliveryRequest`   
`python test.py paystub`   

Scale Test:   
`python test.py deliveryRequest scale`  
