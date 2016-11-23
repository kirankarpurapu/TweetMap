import boto.sqs

connect_to_region = boto.sqs.connect_to_region("us-west-2")

# one second visibility timeout
queue = connect_to_region.create_queue('TweetMap', 1) 

print("created a queue with timeout: " + str(queue.get_timeout()))