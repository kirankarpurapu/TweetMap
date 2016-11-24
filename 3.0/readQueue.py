import json
import time
import boto3
from monkeylearn import MonkeyLearn
from configparser import ConfigParser

#Changes Start

#AWS Auth - SQS
sqs = boto3.resource(
    'sqs',
    aws_access_key_id = "AKIAJISODG75YKJSYFLQ",
    aws_secret_access_key = "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",
)
queue = sqs.get_queue_by_name(QueueName='TweetQueue')

#AWS Auth - SNS
sns = boto3.resource(
    'sns',
	aws_access_key_id="AKIAJISODG75YKJSYFLQ",
	aws_secret_access_key="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",
)

TweetMap_Topic = sns.Topic('arn:aws:sns:us-west-2:259534586546:TweetMap-Topic')

#MonkeyLearn Auth
ml = MonkeyLearn("2d7318621edc4ea02ea2176f1a79f148d63eb6d2")

def getSentiment(tweetText):
    sentences = [ tweetText ]
    sentimentResult = ml.classifiers.classify("cl_qkjxv9Ly", sentences, sandbox=True).result
    for result in sentimentResult:
        sentiment = result[0]['label']
        return sentiment

# Changes End


def processMessages(results, myQueue):
	try:
		for result in results:	
			message = json.loads(result.body)
			print(message['text'])
			sentiment = getSentiment(message['text'])
			message['sentiment'] = sentiment
			pub = TweetMap_Topic.publish( Message = json.dumps(message))
			print("making a notification for the tweet of sentiment: " + sentiment )
			print("------------------------------")
			#deleting the message from the queue
			result.delete()

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
	results = queue.receive_messages(10)
	print("got " + str(len(results)) +" number of messages")
	if len(results) is 0:
		wait()
	else:
		processMessages(results, queue)
	