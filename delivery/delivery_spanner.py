from google.cloud import pubsub_v1
from google.cloud import spanner
import json
import time

import logging
logging.basicConfig()

subscriber = pubsub_v1.SubscriberClient()
delivery_subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'delivery-0-delivery-request')

spanner_client = spanner.Client()
instance_id = 'cloudpay-db'
instance = spanner_client.instance(instance_id)
database_id = 'cloudpay'
database = instance.database(database_id)

def listen():
	def delivery_callback(message):
		print('Received delivery-request message:')
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		deliver(data)	

	subscriber.subscribe(delivery_subscription_path, callback=delivery_callback)
	print('Listening for messages on: \n{}'.format(delivery_subscription_path))
	while True:
		time.sleep(60)

def deliver(data):
	company_id = data['CompanyId']
	employee_id = data['EmployeeId']
	pay_period = data['PayPeriod']

	query = "SELECT c.CompanyName, e.Name, e.EmployeeSsn, p.PayPeriod, p.Pay " \
		+ "FROM Paystubs p JOIN Company c ON c.CompanyId = p.CompanyId " \
		+ "JOIN Employees e ON e.EmployeeId = p.EmployeeId " \
		+ "WHERE c.CompanyId = {} AND e.EmployeeId = {};".format(company_id, employee_id)
	print(query)

	with database.snapshot() as snapshot:
		results = snapshot.execute_sql(query)
		for result in results:
			paystub = result
			print(paystub)

	paystub_data = {}
	paystub_data['company_name'] = str(paystub[0])
	paystub_data['employee_name'] = str(paystub[1])
	paystub_data['ssn'] = str(paystub[2])
	paystub_data['pay_period'] = str(paystub[3])
	paystub_data['income'] = str(paystub[4])

	paystub_json = json.dumps(paystub_data)

	publisher = pubsub_v1.PublisherClient()
	paystub_delivery_topic_path = publisher.topic_path('cs-385-cloudpay', 'paystub-delivery')
	data = paystub_json.encode('utf-8')
	publisher.publish(paystub_delivery_topic_path, data=data)

if __name__ == '__main__':
	listen()
