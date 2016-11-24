var app = require('express')();
var express = require('express');
var http = require('http').Server(app);
var io = require('socket.io')(http);


var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true }));

// var qs = require('querystring');



app.get('/', function(req, res){
	console.log('new page load request');
	// io.emit('new_tweet_indexed', 'AnewTweet');
  res.sendfile('index.html');
});

app.get('/page', function(req, res){
	console.log(' page1');
	

	io.emit('new_tweet_indexed', 'AnewTweet');

  res.sendfile('index.html');
});


app.post('/notifications', function(req, res){

	io.emit('new_tweet_indexed', 'AnewTweet');
	console.log("emitted");
  res.sendfile('index.html');
});


app.post('/page', function(req, res){
	
	io.emit('new_tweet_indexed', 'AnewTweet');
	console.log("emitted");
  res.sendfile('index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});

http.listen(5000, function(){
  console.log('listening on *:5000');
});