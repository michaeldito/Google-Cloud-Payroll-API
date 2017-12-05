from flask import Flask, Response, request
import json
import datetime
from google.cloud import pubsub_v1

app = Flask(__name__)

paystubs = {}

subscriber = pubsub_v1.SubscriberClient()
paystub_delivery_subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'application-0-paystub-delivery')

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

	msg = ""
	def callback(message):
		print('Received message {}'.format(message))
		message.ack()
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		print('End of Message\n')
		ssn = data['employee_ssn']
		paystubs[ssn] = data

	subscriber.subscribe(paystub_delivery_subscription_path, callback)
	return Response(response=json.dumps(batch, indent=2), status=200, mimetype="application/json")

@app.route("/paystub", methods=['POST', 'GET'])
def paystub():
	batch = request.get_json(force=True)
	print('--- Incoming Request ---')
	print json.dumps(batch,indent=4)
	print('---- End of Request ----')

	data = json.loads(batch)
	ssn = data['employee_ssn']

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
