from boto.sqs.message import Message
import boto.sqs
import boto.sns
import json
import time
from alchemyapi import AlchemyAPI
import elasticsearch


conn = boto.sqs.connect_to_region("us-west-2")
SNSconn = boto.sns.connect_to_region("us-west-2")

myQueue = conn.get_queue('TweetQueue')
TweetMap_Topic = 'arn:aws:sns:us-west-2:259534586546:TweetMap-Topic'

alchemyapi = AlchemyAPI()

# es = elasticsearch.Elasticsearch()

myQueue.set_message_class(Message)

def processMessages(results, myQueue):
	try:
		for result in results:	
			message = json.loads(result.get_body())
			print(message['text'])
			print("------------------------------")
			response = alchemyapi.sentiment("text", message['text'])
			sentiment = response["docSentiment"]["type"]
			message['sentiment'] = sentiment
			# es.index(index='myposts', doc_type='mytweets' , body= message)
			pub = SNSconn.publish( topic = TweetMap_Topic, message = json.dumps(message))
			print("making a notification for the tweet of sentiment: " + sentiment )
			print("------------------------------")
			#deleting the message from the queue
			myQueue.delete_message(result)
		print("wait start")	
		time.sleep(10)
		print("wait end")
	except AttributeError as e:
		print ("Encountered a key AttributeError: "+str(e))
		pass
	except KeyError as e:
		print ("Encountered a key error: "+str(e))
		pass
	except Exception as excpt:
		print("encountered an exception while getting the sentiment " + str(excpt))
		pass		

def wait():
	print("starting to wait for 30 seconds")
	time.sleep(30)
	print("finished sleeping for 30 seconds")


while True:
	results = myQueue.get_messages(10)
	print("got " + str(len(results)) +" number of messages")
	if len(results) is 0:
		wait()
	else:
		processMessages(results, myQueue)	
	