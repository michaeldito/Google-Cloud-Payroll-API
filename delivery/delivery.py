from google.cloud import pubsub_v1
import json
import time
import MySQLdb
import logging
logging.basicConfig()

subscriber = pubsub_v1.SubscriberClient()
delivery_subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'delivery-0-delivery-request')

db = MySQLdb.connect('35.197.29.57', 'root', 'cs385', 'cloudpay')
cursor = db.cursor()

def delivery():
	msg = ""
	def callback(message):
		print('Received message {}'.format(message))
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		print('End of Message\n')
		get_data(data)	

	subscriber.subscribe(delivery_subscription_path, callback=callback)
	print('Listening for messages on {}'.format(delivery_subscription_path))
	while True:
		time.sleep(60)

def get_data(data):
	errors = False
	company_id = data['company_id']
	employee_id = data['employee_id']
	pay_period = data['pay_period']
	query = "SELECT c.company_name, e.name, e.employee_ssn, p.pay_period, p.income " \
		+ "FROM paystubs_table p " \
		+ "JOIN company_table c ON c.company_id = p.company_id " \
		+ "JOIN employee_table e ON e.employee_id = p.employee_id " \
		+ "WHERE c.company_id = {} AND e.employee_id = {};".format(company_id, employee_id)
	print(query)
	result = cursor.execute(query)
	paystub = cursor.fetchone()

	paystub_data = {}
	paystub_data['company_name'] = str(paystub[0])
	paystub_data['employee_name'] = str(paystub[1])
	paystub_data['ssn'] = str(paystub[2])
	paystub_data['income'] = str(paystub[4])

	paystub_json = json.dumps(paystub_data)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'paystub-delivery')
	data = paystub_json.encode('utf-8')
	publisher.publish(topic_path, data=data)

if __name__ == '__main__':
	delivery()
