
from __future__ import print_function
from flask import Flask, redirect, url_for, request, render_template, Response
from requests_aws4auth import AWS4Auth
import json
import os
import elasticsearch
import urllib2
import flask



#SNS subject : TweetMap

#from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
# es = elasticsearch.Elasticsearch()

host = 'search-tweetmap-kbz75cdphmmyi74fzn74suhsye.us-west-2.es.amazonaws.com'
AWS_ACCESS_KEY = "AKIAJISODG75YKJSYFLQ"
AWS_SECRET_KEY = "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"
REGION = "us-west-2"

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
@app.route('/notifications',methods = ['POST', 'GET'])
def processNotification():
	if request.method == 'POST':
		print("------------------------------")
		hdr = request.headers.get('X-Amz-Sns-Message-Type')
		print("header : " + str(hdr))
		jsonData = json.loads(request.data)
		if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in jsonData:
			URL = jsonData['SubscribeURL']
			print("URL : " + URL)
			urllib2.urlopen(URL).read()
			print("Made a get request to the confirmation URL")
		print("------------------------------")
		if hdr == 'Notification':
			# messageJSON = json.loads(jsonData['Message'])
			print("Notification content \n" + jsonData['Message'])
			es.index(index='myposts', doc_type='mytweets', body= jsonData['Message'])
			print("indexed into elastic search")
		print("-------------------------------")

	response = Response("200OK")
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response	



@app.route ('/',methods = ['POST', 'GET'])
def processInput():
	# optionsTemplateCode = makeOptionsData()
	if request.method == 'POST':
		searchKey = request.form['keyword']
		type_txt= request.form['happy']
		isnormal=request.form['isnormal']
		dist=request.form['distance']
		lat=""
		lng=""
		if(isnormal is "2"):
			lat=str(request.form['lat'])
			lng=str(request.form['lng'])
			
		print("success ", searchKey+" : "+type_txt)

		#some twitter elastic search matching
		tweets = getMatchingTweets(searchKey,type_txt,isnormal,lat,lng,dist)	
	# should improve on this logic	
	else:
		print ("NOT A POST REQUEST", "returning empty tweet array")
		tweets = {}	
	return render_template('tweetmap.html', tweets = tweets)


def myReplace(myString):
	dictionary = {"-":  r"\-", "]":  r"\]", "\\": r"\\", "^":  r"\^", "$":  r"\$", "*":  r"\*", ".":  r"\.", "'":  r"\'", '"':  r'\"'}
	for character in myString:
		if character in dictionary:
			myString = myString.replace(character, dictionary[character])
	return myString		

def getMatchingTweets(search_key,type_txt,isnormal,lat,lng,dist):
	listOfTweetsAsList = []
	data_dict = {}
	resultDict={}
	print("START")
	#bodyOfRequest = '{"query":{"query_string":{"query": "' + search_key+ '"}}}'
	bodyOfRequest=""
	firstPart = '{"size":3000, "query":{"query_string":{"query":'
	lastPart = ' }}}'
	if(isnormal is "1"):
		#bodyOfRequest = '{"fields" : ["latitude", "longitude"],"query":{"term":{"search_key" : "'+search_key.lower()+'" }},"size":3000}'
		
		bodyOfRequest = firstPart+'"'+search_key+'"'+ lastPart
	else:
		#bodyOfRequest = '{"fields" : ["latitude", "longitude"],"query":{"filtered": {"query": {"match_all": {}},"filter": {"and": [{"geo_distance" : {"distance" : "'+dist+'km","pin.location": ['+lng+','+lat+']} },{"term":{"search_key" : "'+search_key.lower()+'" }}] }}},"size":3000}'
		bodyOfRequest = firstPart+'"'+search_key+'"'+ lastPart
	print ("BODY" , bodyOfRequest)
	res = es.search(index="myposts", doc_type="mytweets", body = bodyOfRequest)
	#query_string = "search_key:%s"% search_key
	#res = es.search(index="posts", q=query_string, size=2000)
	print("%d documents found" % res['hits']['total'])
	# print("[hits][hits] count " , res['hits']['hits'])
	print("Len of results is %d " %len(res['hits']['hits']))
	for doc in res['hits']['hits']:
		#print("From elatic search"+doc['_source']['text'])
		data_dict = {}
		print("*************")
		data_dict['name'] = doc['_source']['userName']
		data_dict['text'] = doc['_source']['text']
		data_dict['date'] = doc['_source']['date']
		data_dict['latitude'] = doc['_source']['latitude']
		data_dict['longitude'] = doc['_source']['longitude']
		data_dict['sentiment'] = doc['_source']['sentiment']
	
		listOfTweetsAsList.append(data_dict)

	resultDict['search_key']=search_key
	resultDict['type_txt']=type_txt
	resultDict['dist']=dist
	resultDict['lat']=lat
	resultDict['lng']=lng
	resultDict['isnormal']=isnormal
	resultDict['result']=listOfTweetsAsList

	if res['hits']['total'] is 0:
		print ("SORRY, NO MATCHING TWEETS FOUND")
		message = "NO_TWEETS"
		resultDict['search_key'] = search_key
		resultDict['type_txt']=type_txt
		resultDict['dist']=dist
		resultDict['lat']=lat
		resultDict['lng']=lng
		resultDict['isnormal']=isnormal
		resultDict['message'] = message
		resultDict['result'] = None
		resultDict['sentiment'] = None
		#tweets = json.dumps(data_dict)
		# dataToReturn = stringEscape(str(json.dumps(resultDict))) 
		dataToReturn = resultDict
		#print ("DATA to return : " , dataToReturn)
		return dataToReturn
	else:
		print ("HORRAY!!, FOUND A FEW MATCHING TWEETS for " + search_key)
		resultDict['message'] = "SUCCESS"
		# dataToReturn = stringEscape(str(json.dumps(resultDict)))
		# dataToReturn = str(json.dumps(resultDict)) 
		# print("RETURNING ******************* " , resultDict ," to the front end")
		dataToReturn = resultDict
		#print ("DATA to return : " , dataToReturn)
		# print(type(dataToReturn))
		# return dataToReturn
		# return json.dumps(resultDict)
		# reponseData = Response(response = resultDict, status = 200, mimetype = "application/json")
		# return responseData
		return flask.jsonify(**resultDict)

		
def stringEscape(myString):
	delete_chars=''.join(chr(i) for i in xrange(32))                        
	return myString.translate(None,delete_chars)
	# return myString.translate(myString.maketrans({"-":  r"\-", "]":  r"\]", "\\": r"\\", "^":  r"\^", "$":  r"\$", "*":  r"\*", ".":  r"\.", "'":  r"\'", '"':  r'\"'}))


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug = True)