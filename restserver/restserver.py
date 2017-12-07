from flask import Flask, Response, request
import json
import datetime
from google.cloud import pubsub_v1

import logging
logging.basicConfig()

import socket
ip = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)

paystubs = {}

subscriber = pubsub_v1.SubscriberClient()
paystub_delivery_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'application-0-paystub-delivery')

#msg = ""
def paystub_delivery_callback(message):
	print('Received paystub-delivery message')
	message.ack()
	data = json.loads(message.data)
	print json.dumps(data, indent=2)
	ssn = int(data['ssn'])
	paystubs[ssn] = data
	print('New paystubs entry: {} => {}'.format(str(ssn), str(paystubs[ssn])))

subscriber.subscribe(paystub_delivery_sub_path, callback=paystub_delivery_callback)

@app.route("/submit", methods=['POST', 'GET'])
def submit():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()
	incoming_data['Internal IP'] = ip
	print('--- New Timesheet Data Received ---')
	print json.dumps(incoming_data,indent=4)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-timesheets')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(incoming_data, indent=2), status=200, mimetype="application/json")

@app.route("/createCompany", methods=['POST', 'GET'])
def create_company():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()
	incoming_data['Internal IP'] = ip
	print('--- New Company Data Received ---')
	print json.dumps(incoming_data,indent=4)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-new-company')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(incoming_data, indent=2), status=200, mimetype="application/json")

@app.route("/addEmployee", methods=['POST', 'GET'])
def add_employee():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()
	incoming_data['Internal IP'] = ip
	print('--- New Employee Data Received ---')
	print json.dumps(incoming_data,indent=4)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'insert-new-employee')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(incoming_data, indent=2), status=200, mimetype="application/json")


@app.route("/deliveryRequest", methods=['POST', 'GET'])
def delivery_request():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()
	incoming_data['Internal IP'] = ip
	print('--- Paystub Delivery Request ---')
	print json.dumps(incoming_data,indent=4)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'delivery-request')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(incoming_data, indent=2), status=200, mimetype="application/json")

@app.route("/paystub", methods=['POST', 'GET'])
def paystub():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()
	incoming_data['Internal IP'] = ip
	print('--- Paystub Pickup Request ---')
	print json.dumps(incoming_data,indent=4)

	ssn = incoming_data['ssn']
	paystub = paystubs[ssn]

	return Response(response=json.dumps(paystub, indent=2), status=200, mimetype="application/json")

@app.route("/calculateAccruals", methods=['POST', 'GET'])
def calculate_accruals():
	incoming_data = request.get_json(force=True)
	incoming_data['Time Received'] = datetime.datetime.utcnow().isoformat()	
	incoming_data['Internal IP'] = ip
	print('--- Calculate Accruals Request ---')
	print json.dumps(incoming_data,indent=4)

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path('cs-385-cloudpay', 'calculate-accruals')
	data = request.data.encode('utf-8')
	publisher.publish(topic_path, data=data)

	return Response(response=json.dumps(incoming_data, indent=2), status=200, mimetype="application/json")


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
