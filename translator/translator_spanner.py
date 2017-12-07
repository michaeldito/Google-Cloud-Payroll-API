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

spanner_client = spanner.Client()
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
	
	print('Listening for messages on:\n{}\n{}\n{}'.format(timesheet_sub_path, insert_new_company_sub_path, insert_new_employee_sub_path))
	while True:
		time.sleep(60)

def translate_new_company(data):
	company_name = data["CompanyName"]
	company_id = data['CompanyId']
	query = "INSERT INTO Company (CompanyName, CompanyId) VALUES (\'{}\', {});".format(company_name, company_id)
	print(query)
	with database.batch() as batch:
		batch.insert(
			table='Company', 
			columns=('CompanyName', 'CompanyId'), 
			values=[(company_name, company_id)])
	print('Company was inserted successfully')
 
def translate_new_employee(data):
	for record in data['employees']:
		employee_id = record['EmployeeId']
		employee_ssn = record['EmployeeSsn']
		company_id = record['CompanyId']
		hourly_pay_rate = record['HourlyPayRate']
		name = record['Name']
		query = "INSERT INTO Employees (EmployeeId, EmployeeSsn, CompanyId, HourlyPayRate, Name)' \
			+ ' VALUES ({},{},{}, \'{}\');".format(employee_id, employee_ssn, company_id, hourly_pay_rate, name)
		print(query)
		with database.batch() as batch:
			batch.insert(
				table='Employees', 
				columns=('EmployeeId', 'EmployeeSsn', 'CompanyId', 'HourlyPayRate', 'Name'),
				values=[(employee_id, employee_ssn, company_id, hourly_pay_rate, name)])
	print('Employee(s) inserted successfully')

def translate_new_timesheet(data):
	company_id = data['CompanyId']
	pay_period = data['PayPeriod']
	for record in data['records']:
		timesheet_id = record['TimesheetId']
		date = record['Date']
		hours = record['HoursWorked']
		employee_id = record['EmployeeId']
		work_type = record['Type']
		query = 'INSERT INTO Timesheets (TimesheetId, EmployeeId, CompanyId, HoursWorked, Type, Date, PayPeriod)' \
			+ ' VALUES ({}, {}, {}, {}, \'{}\', \'{}\', \'{}\');'.format(
			timesheet_id, employee_id, company_id, hours, work_type, date, pay_period)
		print(query)
		with database.batch() as batch:
			batch.insert(
				table='Timesheets',
				columns=('TimesheetId', 'EmployeeId', 'CompanyId', 'HoursWorked', 'Type', 'Date', 'PayPeriod'),
				values=[(timesheet_id, employee_id, company_id, hours, work_type, date, pay_period)])
	print('Timesheet(s) inserted successfully')

if __name__ == '__main__':
	listen()

