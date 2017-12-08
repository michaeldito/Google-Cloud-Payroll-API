from google.cloud import pubsub_v1
from google.cloud import spanner
import json
import time

import logging
logging.basicConfig()

subscriber = pubsub_v1.SubscriberClient()
calculate_accruals_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'accruals-0-calculate-accruals')

spanner_client = spanner.Client()
instance_id = 'cloudpay-db'
instance = spanner_client.instance(instance_id)
database_id = 'cloudpay'
database = instance.database(database_id)

def listen():
	def calculate_accruals_callback(message):
		print('Received calulate-accruals message:')
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		calculate_accruals(data)

	subscriber.subscribe(calculate_accruals_sub_path, callback=callback)
	print('Listening for messages on {}'.format(calculate_accruals_sub_path))
	while True:
		time.sleep(60)

def calculate_accruals(data):
	company_id = data['company_id']
	pay_period = data['pay_period']

	hours_worked =  {}
	pay_rates = {}
	total_pay = {}

	'''First select the timesheets for the company in the requested pay period'''
	with database.snapshot() as snapshot:
		query = "SELECT * FROM Timesheets WHERE CompanyId = {} and PayPeriod = \'{}\';".format(company_id, pay_period)
		print(query)
		results = snapshot.execute_sql(query)
		for result in results:
			employee_id = int(result[0])
			hours = float(result[2])
			if employee_id not in hours_worked:
				hours_worked[employee_id] = hours
			else:
				hours_worked[employee_id] += hours

	'''Then map the hourly pay rate to each employee in the company'''
	for employee_id, hours in hours_worked.iteritems(): 
		with datebase.snapshot() as snapshot:	
			query = "SELECT HourlyPayRate from Employee WHERE EmployeeId = {} and CompanyId = {};".format(employee_id, company_id)
			print(query)
			result = snapshot.execute_sql(query)
			'''After this for loop, rate will be a list containing the hourly pay rate for the current employee.'''
			for result in results:
				rate = result
			pay_rates[employee_id] = int(rate[0])
			for employee_id, hours in hours_worked.iteritems():
				total_pay[employee_id] = hours * pay_rates[employee_id]
			for employee_id, pay in total_pay.iteritems():
				query = "INSERT INTO Paystubs (EmployeeId, CompanyId, PayPeriod, Pay) VALUES ({}, {}, \'{}\', {});".format(
					employee_id, company_id, pay_period, total_pay[(e, c)])
				print(query)
				with database.batch() as batch:
					batch.insert(
						table='Paystubs',
						columns=('EmployeeId', 'CompanyId', 'PayPeriod', 'Pay'),
						values=[(employee_id, ccompany_id, pay_period, total_pay[employee_id])])

if __name__ == '__main__':
	listen()
