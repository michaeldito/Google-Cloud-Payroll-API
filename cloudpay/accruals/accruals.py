from google.cloud import pubsub_v1
import MySQLdb
import json
import time

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'accruals-0-calculate-accruals')

db = MySQLdb.connect('35.225.146.232', 'root', 'cs385', 'pay-stubs')
cursor = db.cursor()

def get_data():
	msg = ""
	def callback(message):
		print('Received message: {}'.format(message))
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		print('End of Message\n')
		calculateAccruals(data)

	subscriber.subscribe(subscription_path, callback=callback)
	print('Listening for messages on {}'.format(subscription_path)
	while True:
		time.sleep(60)

def calculate_accruals(data):
	errors = False
	company_id = data['company_id']
	pay_period = data['pay_period']
	query = 'SELECT FROM timesheet_table WHERE company_id = {} and pay_period = \'{}\';'.format(company_id, pay_period)
	print(query)
	result = cursor.execute(query)
	if not result:
		errors = True
	print('Errors: {}'.format(errors))

	results = cursor.fetchall()
	hours_worked =  {}
	for result in results:
		(employee_id, company_id) = int(result[1]), int(result[2])
		hours = float(result[3])
		if employee_id not in hours_worked:
			hours_worked[(employee_id, company_id)] = hours
		else:
			hours_worked[(employee_id, company_id)] += hours

	query = "SELECT hourly_pay_rate from employee_table WHERE employee_id = {} and company_id = {};"
	result = cursor.execute(query)
	pay_rate = cursor.fetchone()
	pay_rate = float(pay_rate[0])
	for (employee_id, company_id), hours in hours_worked.iteritems(): 
		query = "SELECT hourly_pay_rate from employee_table WHERE employee_id = {} and company_id = {}".format(employee_id, company_id)
		result = cursor.execute(query)
		rate = cursor.fetchone()
		rate = float(rate[0])
		pay_rates[(employee_company_id)] = rate

	for (employee_id, company_id), hours in hours_worked.iteritems():
		pay_stubs[(employee_id, company_id)] = hours * pay_rates[(e, c)]

	for (e, c), pay in pay_stubs.iteritems():
		query = "INSERT INTO paystubs_table (employee_id, company_id, pay_period, income) VALUES ({}, {}, \'{}\', {}".format(e, c, pay_period, pay_stubs[(e, c)])

if __name__ == '__main__':
	get_data()
