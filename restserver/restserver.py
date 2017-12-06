from flask import Flask, Response, request
import json
import datetime
from google.cloud import pubsub_v1

import logging
logging.basicConfig()

app = Flask(__name__)

paystubs = {}

subscriber = pubsub_v1.SubscriberClient()
paystub_delivery_subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'application-0-paystub-delivery')

msg = ""
def callback(message):
	print('Received message {}'.format(message))
	print('Ackknowledging...')
	message.ack()
	print('Printing with json.loads...')
	data = json.loads(message.data)
	print json.dumps(data, indent=2)
	print('Adding to paystubs')
	ssn = int(data['ssn'])
	print('Checking ssn type')
	print(type(ssn))
	paystubs[ssn] = data
	print(paystubs[ssn])

subscriber.subscribe(paystub_delivery_subscription_path, callback=callback)

@app.route("/submit", methods=['POST', 'GET'])
def submit():
	batch = request.get_json(force=True)
	batch['timestamp'] = datetime.datetime.utcnow().isoformat()
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')
	
	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-timesheets')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")

@app.route("/createCompany", methods=['POST', 'GET'])
def create_company():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-new-company')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")

@app.route("/addEmployee", methods=['POST', 'GET'])
def add_employee():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-new-employee')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")


@app.route("/deliveryRequest", methods=['POST', 'GET'])
def delivery_request():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'delivery-request')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")

@app.route("/paystub", methods=['POST', 'GET'])
def paystub():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	data = request.get_json(force=True)
	print('Inside paystub\nPrinting request.get_json()')
	print(data)
	ssn = data['ssn']

	paystub = paystubs[ssn]

	return Response(response=json.dumps(paystub, indent=2), status=200, mimetype="application/json")

@app.route("/calculateAccruals", methods=['POST', 'GET'])
def calculate_accruals():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'calculate-accruals')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
