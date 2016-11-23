import json
import random
import tweepy
import time
import datetime


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# import elasticsearch
import collections
import boto3
from boto.sqs.message import Message
import boto.sqs

# conn = boto.sqs.connect_to_region("us-west-2")

# myQueue = conn.get_queue('TweetQueue1')

sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='TweetQueue')


consumer_key="4SXhZPURJLXu9RnhkQkzyuwrM"
consumer_secret="Q3B85IwmCgRfzF5hESZqRKm1FVbnQqZvesyrj6xvKJsfXyjy4H"
access_token="465606029-5j06IPwdtoO1vrMA6EzHZhO3c2ryu0YpoJAvKsOu"
access_token_secret="VT8NcwwT1stSZ0S2XvP8t476kvTOnepRswlZfNZqsd6sG"
search_key_array = ["TheWalkingDead", "Bentancur", "india", "DDoS", "apple", "dhoni", "chelsea", "facebook", "trump", "election", "hillary","RespectJustin","Drake","war","google"]
#search_key_array = ["badminton", "cricket", "hockey", "soccer", "football"]
track_string = search_key_array[0]
for index in range(len(search_key_array)-1):
	track_string += ",%s" % search_key_array[index+1]


class StdOutListener(StreamListener):
	print ("class created")
	def on_data(self, data):
		# es = elasticsearch.Elasticsearch()
		if data is not None:
			dict = collections.OrderedDict()
			loc = collections.OrderedDict()
			tweet = json.loads(data)
			try:
				if tweet['id']:
					tweet_id = tweet['id']
				if tweet['text']:
					text= tweet['text']
				else :
					print("no text")
					return True
				if tweet['created_at']:
					dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
					date = str(datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S"))
				if tweet['user']:
					userName= str(tweet['user']['name'])
					userScreenName= str(tweet['user']['screen_name'])
				if tweet['coordinates']:
					coordinates = tweet['coordinates']['coordinates']
					longitude = coordinates[0]
					latitude = coordinates[1]
				elif tweet['place'] and tweet['place']['bounding_box'] and tweet['place']['bounding_box']['coordinates']:
					coordinates = tweet['place']['bounding_box']['coordinates'][0]
					longitude = (coordinates[0][0] + coordinates[2][0])/2
					latitude = (coordinates[0][1] + coordinates[2][1])/2
				else :
					print("no lat long")
					return True
				#temparr=[tweet_id.encode("utf-8"),date.encode("utf-8"),userName.encode("utf-8"),userScreenName.encode("utf-8"),text.encode("utf-8"),longitude.encode("utf-8"),latitude.encode("utf-8")]
				#dict['tweetId'] = tweet_id
				dict['text'] = text.replace("'","\'")
				dict['date'] = date
				dict['userName'] = userName
				dict['userScreenName'] = userScreenName
				dict['latitude'] = latitude
				dict['longitude'] = longitude
				#dict['longitude'] = longitude
				#loc['location']=[longitude,latitude]
				dict['pin']={ 'location': str(latitude)+","+str(longitude)}
				search_key = []
				for key in search_key_array:
					if key.lower() in text.lower():
						search_key.append(key.lower())
				dict['search_key'] = search_key
				print (search_key)
				if (len(search_key)>0):
					jsonArray = json.dumps(dict)
					#print(temparr)
					print(jsonArray)	
					#index = index's size 

					response = queue.send_message(MessageBody=jsonArray)
					# The response is NOT a resource, but gives you a message ID and MD5
					print("-----------------------------------")
					print(response.get('MessageId'))
					print(response.get('MD5OfMessageBody'))
					print("-----------------------------------")
					# es.index(index='myposts', doc_type='mytweets' ,id=tweet_id, body= jsonArray)
					# print ("added into elastic search")

			except AttributeError as e:
				print ("Encountered a key AttributeError: "+str(e))
				return True		
			except KeyError as e:
				print ("Encountered a key error: "+str(e))
				return True	
			except Exception as e:
				print("err "+str(e))
				return True


		return True

	def on_error(self, status):
		print ("err: "+str(status))
		if status==420:
			return False
		return True


		
def main():
	listener = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, listener)
	print("ready")
	while 1==1:
		while True:
			try:
				stream.filter(track=search_key_array, locations=[-180,-90,180,90])
				print("done")
				break
			except tweepy.TweepError:
				print("tweepy error")
				print("error. sleeping in for :"+str(nsecs))
				nsecs=random.randint(60,63)
				time.sleep(nsecs)
		nmsecs=random.randint(60,63)
		print("error. sleeping out for :"+str(nmsecs))
		time.sleep(nmsecs)
			
if __name__ == '__main__':
	main()
