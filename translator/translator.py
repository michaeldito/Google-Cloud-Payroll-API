from google.cloud import pubsub_v1
import MySQLdb
import time
import json
import logging
logging.basicConfig()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-timesheets')

# subscriber for the insert-new company
insert_NC_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-insert-new-company') 
insert_NE_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'translator-0-insert-new-employee')
#insert_NT_sub_path = subscriber.subscription_path('cs-385-cloudpay', 'insert-timesheets')    

#publisher = pubsub_v1.PublisherClient()
#topic_path = publisher.topic_path('cs-385-cloudpay', 'Batch-Status')

db = MySQLdb.connect('35.197.29.57', 'root', 'cs385', 'cloudpay')
cursor = db.cursor()

def get_data():
	msg = ""
	def new_timesheet_callback(message):
		print('Received message: {}'.format(message))
		message.ack() # change wen we get sql status from insert
		data = json.loads(message.data)
		print json.dumps(data, indent=2)
		print('End of Message\n')
		#translate(data)
		translate_new_timesheet(data)
	def new_company_callback(message) :
		print("in new_company_callback")
		message.ack() # change wen we get sql status from insert		
		data = json.loads(message.data)		
		translate_new_company(data)	

	def new_emp_callback(message):
		print("in new_emp_callback")
		message.ack()
		data = json.loads(message.data)
		translate_new_emp(data)

	# assuming we can call the subscriber on multiple subscription path with different call back	
	subscriber.subscribe(subscription_path, callback=new_timesheet_callback)
	subscriber.subscribe(insert_NC_sub_path, callback=new_company_callback)
	subscriber.subscribe(insert_NE_sub_path, callback=new_emp_callback)
	#subscriber.subscribe(insert_NT_sub_path, callback=new_timesheet_callback)
	
	print('Listening for messages on {}'.format(subscription_path))
	while True:
		time.sleep(60)

def translate_new_company(data):
	errors = False
	company_name = data["company_name"]
	query = 'INSERT INTO company_table (company_name) VALUES (\'{}\')'.format(company_name) + ';'
	print(query)
	print('Inserting into cloudpay db, Company_Table ...')
	result = cursor.execute(query);
	db.commit()
	if not result:
		errors = True
		print(' FAILED')
	else:
		print(' SUCCESS, inserted into Company_Table') 
	# todo publish a response 

 
def translate_new_emp(data):
	errors = False
	for record in data['employees']:
		employee_ssn = record['employee_ssn']
		company_id = record['company_id']
		hourly_pay_rate = record['hourly_pay_rate']
		name = record['name']
		query = 'INSERT INTO employee_table (employee_ssn, company_id, hourly_pay_rate, name)'\
			+ ' VALUES ({},{},{}, \'{}\')'.format(employee_ssn, company_id, hourly_pay_rate, name) +';'
		print(query)
                print('Inserting into cloudpay db, Employee table...')
		result = cursor.execute(query);
		db.commit()
                if not result:
                        errors = True
                        print(' FAILED')
                else:
                        print(' SUCCESS')	

def translate_new_timesheet(data):
	errors = False
	company_id = data['company_id']
	pay_period = data['pay_period']
	for record in data['records']:
		date = record['date']
		hours = record['hours']
		employee_id = record['employee_id']
		work_type = record['type']
		query = 'INSERT INTO timesheet_table (employee_id, company_id, hours, type, date, pay_period)' \
			+ ' VALUES ({}, {}, {}, \'{}\', \'{}\', \'{}\')'.format(employee_id, company_id, hours, work_type, date, pay_period) \
			+ ';'
		print(query)
		print('Inserting into cloudpay db, timesheet table...'),
		result = cursor.execute(query);
		db.commit()
		if not result:
			errors = True
			print(' FAILED')
		else:
			print(' SUCCESS')		

	#print('Errors: {}'.format(errors))
	#if not errors:
	#	publisher.publish(topic_path, 'Successfully received your timesheet data')
	#else:
	#	publisher.publish(topic_path, 'Bad timesheet data. Check your JSON values\n {}'.format(json.dumps(data, indent=4)))

if __name__ == '__main__':
	get_data()

