import boto3

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName = 'TweetMap')
#to purge the queue
queue.purge()