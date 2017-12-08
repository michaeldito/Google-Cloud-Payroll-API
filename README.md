# A RESTful Auto-Scaling Payroll API

A scalable REST API to calculate your payroll, using Flask, Google Cloud, and Pub/Sub.
Two scripts are provided for each component, one will use Google SQL, the other will
use Google Cloud Spanner.

## Google Cloud SQL
If you opt for Cloud SQL as your database, you must install the cloud sql proxy.
https://cloud.google.com/sql/docs/mysql/sql-proxy

## Google Cloud Spanner
If you opt for Cloud Spanner as your database, go ahead and create the instance.
https://cloud.google.com/spanner/docs/create-manage-instances

Now use spanner.sql to create your tables.

## Base Image
A simple way to set up Application, Accruals, Delivery, and Translator is to create
a base image with all libraries needed. Install all requirements with:
`pip install -r requirements`
Now create your base image (make sure it contains the sql-proxy if you are using Cloud SQL).

## Instance Template
In order to add a Load Balancer you need a Managed Instance Group. To create a Managed Instance
Group, you need an Instance Template that defines the properties of the group.
https://cloud.google.com/compute/docs/instance-templates/create-instance-templates

## Managed Instance Group
Now, create your Managed Instance Group using your Instance Template.
https://cloud.google.com/compute/docs/instance-groups/distributing-instances-with-regional-instance-groups

## Load Balancer
You are now ready to enable the Load Balancer.   
https://cloud.google.com/compute/docs/load-balancing/network/

## Auto-Scaling
Now that the Load Balancer is enabled, you have the option to turn on Auto-Scaling.
https://cloud.google.com/compute/docs/autoscaler/scaling-cpu-load-balancing

## Pub/Sub
In order to use Pub/Sub, a service account key with Pub/Sub access should be set up.

Next, you'll need to create the following topics:   
* insert-new-company   
* insert-new-employee    
* insert-timesheets
* calculate-accruals   
* delivery-request   
* paystub-delivery

Now you'll need to create the subscriptions to these topics:
* application-0-paystub-delivery   
* accruals-0-calculate-accruals   
* delivery-0-delivery-request   
* translator-0-timesheets   
* translator-0-insert-new-company   
* translator-0-insert-new-employee  

**The service should now be ready.**

## Startup Scripts
Each component has a startup script, here are their locations:

Application - `restserver/start-server.sh`

The following components have 2 options: one script is for the SQL database, the other is for Spanner.     
Accruals    - `accruals/accruals.py` 		    `accruals/accruals_spanner.py`       
Delivery    - `delivery/delivery.py`		    `delivery/delivery_spanner.py`         
Translator  - `translator/translator.py`  	`translator/translator_spanner.py`       

**Remember to star the cloud sql proxy if you are using Cloud SQL.**   
https://cloud.google.com/sql/docs/mysql/connect-compute-engine

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
