from boto.sqs.message import Message
import boto.sqs

conn = boto.sqs.connect_to_region("us-west-2")

myQueue = conn.get_queue('TweetQueue')

print("finished connecting to " + str(myQueue))

m = Message()
m.message_attributes = {
  "name1": {
         "data_type": "String",
         "string_value": "I am a string"
     },
     "name2": {
         "data_type": "Number",
         "string_value": "12"
     }
}

m.set_body('This is a test message 2.')
response = myQueue.write(m)


print("wrote this message: " + m.get_body()+ " id: " + str(response.id) + " and its MD5 is " + str(response.md5))



# import boto3

# # To create a new sqs 
# # queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# #connecting to an existing queue with the name 'TweetMap'
# sqs = boto3.resource('sqs')
# queue = sqs.get_queue_by_name(QueueName = 'TweetMap')

# print(queue.url)


# #send a single message
# #response = queue.send_message(MessageBody='world')

# # The response is NOT a resource, but gives you a message ID and MD5

# #print("Message ID:" + response.get('MessageId'))
# #print("MD5 of messageBody:" + str(response.get('MD5OfMessageBody')))


# #sending a batch of messages
# response = queue.send_messages(Entries=[
#     {
#         'Id': '1',
#         'MessageBody': 'boto1',
#         'MessageAttributes': {
#             'Author': {
#                 'StringValue': 'Kiran',
#                 'DataType': 'String'
#             }
#         }
#     }
#     # },
#     # {
#     #     'Id': '2',
#     #     'MessageBody': 'boto2',
#     #     'MessageAttributes': {
#     #         'Author': {
#     #             'StringValue': 'Kiran',
#     #             'DataType': 'String'
#     #         }
#     #     }
#     # }
# ])

# print(response.get('Failed'))


# # Process messages by printing out body and optional author name

# # for message in queue.receive_messages(MessageAttributeNames=['All']):
# #     # Get the custom author message attribute if it was set
# #     author_text = ''
# #     if message.message_attributes is not None:
# #     	print("one None")
# #         author_name = message.message_attributes.get('Author').get('StringValue')
# #         if author_name:
# #             author_text = ' ({0})'.format(author_name)

# #     # Print out the body and author (if set)
# #     print('Hello, {0}!{1}'.format(message.body, author_text))


# # to process messages from the queue

# # for message in queue.receive_messages( AttributeNames=[
# #         'All'
# #     ]):
# # 	print("Read a message")
# # 	print('Hello, '.format(message.body))



