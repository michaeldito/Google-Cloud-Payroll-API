from google.cloud import pubsub_v1
from google.cloud import spanner
import time
import json

import logging
logging.basicConfig()

subscriber = pubsub_v1.SubscriberClient()

timesheet_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-timesheets')
insert_new_company_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-insert-new-company') 
insert_new_employee_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-insert-new-employee')

panner_client = spanner.Client()
instance_id = 'cloudpay-db'
instance = spanner_client.instance(instance_id)
database_id = 'cloudpay'
database = instance.database(database_id)

def listen():
#	msg = ""
	def new_timesheet_callback(message):
		print('Received insert-new-timesheet message:')
		message.ack() # change wen we get sql status from insert
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		translate_new_timesheet(data)

	def new_company_callback(message) :
		print('Received insert-new-company message:')
		message.ack() # change wen we get sql status from insert		
		data = json.loads(message.data)		
		print json.dumps(data, indent=2)
		translate_new_company(data)	

	def new_employee_callback(message):
		print('Received insert-new-employee message:')
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		translate_new_employee(data)

	# assuming we can call the subscriber on multiple subscription path with different call back	
	subscriber.subscribe(timesheet_sub_path, callback=new_timesheet_callback)
	subscriber.subscribe(insert_new_company_sub_path, callback=new_company_callback)
	subscriber.subscribe(insert_new_employee_sub_path, callback=new_employee_callback)
	
	print('Listening for messages on:\n{}\n{}\n{}'.format(subscription_path, insert_NC_sub_path, insert_NE_sub_path))
	while True:
		time.sleep(60)

def translate_new_company(data):
	company_name = data["company_name"]
	query = "INSERT INTO Company (CompanyName) VALUES (\'{}\');".format(company_name)
	print(query)
	with database.batch() as batch:
		batch.insert(
			table='Company', 
			columns=('CompanyName'), 
			values=[company_name])
 
def translate_new_employee(data):
	for record in data['employees']:
		employee_ssn = record['employee_ssn']
		company_id = record['company_id']
		hourly_pay_rate = record['hourly_pay_rate']
		name = record['name']
		query = "INSERT INTO Employees (EmployeeSsn, CompanyId, HourlyPayRate, Name)'\
			+ ' VALUES ({},{},{}, \'{}\');".format(employee_ssn, company_id, hourly_pay_rate, name)
		print(query)
		with database.batch() as batch:
			batch.insert(
				table='Employees', 
				columns=('EmployeeSsn', 'CompanyId', 'HourlyPayRate', 'Name'),
				values=[(employee_ssn, company_id, hourly_pay_rate, name)])

def translate_new_timesheet(data):
	company_id = data['company_id']
	pay_period = data['pay_period']
	for record in data['records']:
		date = record['date']
		hours = record['hours']
		employee_id = record['employee_id']
		work_type = record['type']
		query = 'INSERT INTO Timesheet (EmployeeId, CompanyId, Hours, Type, Date, PayPeriod)' \
			+ ' VALUES ({}, {}, {}, \'{}\', \'{}\', \'{}\');'.format(
			employee_id, company_id, hours, work_type, date, pay_period)
		print(query)
		with database.batch() as batch:
			batch.insert(
				table='Timesheet',
				columns=('EmployeeId', 'CompanyId', 'Hours', 'Type', 'Date', 'PayPeriod'),
				values=[(employee_id, company_id, hours, work_type, date, pay_period)])

if __name__ == '__main__':
	listen()

