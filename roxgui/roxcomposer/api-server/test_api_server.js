var http = require('http');
var request = require('supertest');
var apiSrv = require('../src/roxcomposer.js');
var Emitter = require('events').EventEmitter;
var emitter = new Emitter();

var apiPort = 8601;
var dummyPort = 8602;
var dummyMsg = '{"re": "ality"}'; 

function kthxbye() {
	console.log('----- all test successful -----');
	process.exit(0);
}
apiConfig = {
	SYSTEM: {
		port: apiPort
	},
	REST: {
		GET: {
			fortune_cookie: {
				handler: {
					type: 'http',
					options: {
						host: 'localhost',
						port: dummyPort,
						path: '/'
					}
				}
			}
		},
		POST: {
			echo: {
				handler: {
					type: 'process',
					command: ['cat', '-']
				}
			},
			fortune_cookie: {
				handler: {
					type: 'http',
					data: '-',
					options: {
						method: 'POST',
						host: 'localhost',
						port: dummyPort,
						path: '/'
					}
				}
			}
		}
	}
};

// we start a little dummy server to test the http-handler functionality
dummy = new http.Server().on('request', (req, res) => {
	if (req.method === 'GET') {
		res.writeHead(200, {'Content-Length': dummyMsg.length, 'Content-Type': 'application/json'});
		res.write(dummyMsg);
		res.end();
	} else if(req.method === 'POST') {
		var data = '';
		req.on('data', function(chunk) { data += chunk; });
		req.on('end', function() {
			res.writeHead(200, {'Content-Length': data.length, 'Content-Type': 'application/json'});
			res.write(data);
			res.end();
		});
	} else {
		res.writeHead(404);
		res.end();
	}
});
dummy.listen(dummyPort);

srv = apiSrv.new(apiConfig);
request = request(srv);

console.log('----- running tests -----');
console.log('** making a valid GET request **');
request.get('/fortune_cookie')
	.expect('Content-Type', /application\/json/)
	.expect(200, dummyMsg)
	.end(function(err, res) {
		if(err)
			throw err;
		console.log('** got the right answer **');
		emitter.emit('test1');
	});

emitter.on('test1', function() {
	console.log('** GETting invalid path **');
	request.get('/fortune_rookie')
		.expect('Content-Type', /application\/json/)
		.expect(404)
		.end(function(err, res) {
			if(err)
				throw err;
			console.log('** got 404 - good **');
			emitter.emit('test2');
		});
});

emitter.on('test2', function() {
	var testMsg = '{"msg":"blorp"}';
	console.log('** POSTing something to a process **');
	request.post('/echo')
		.send(testMsg)
		.set('Content-Type', 'application/json')
		.expect('Content-Type', /application\/json/)
		.expect(200, testMsg)
		.end(function(err, res) {
			if(err)
				throw err;
			console.log('** got the correct response **');
			emitter.emit('test3');
		});
});

emitter.on('test3', function() {
	var testMsg = '{"msg":"blorp"}';
	console.log('** POSTing something to a http handler **');
	request.post('/fortune_cookie')
		.send(testMsg)
		.set('Content-Type', 'application/json')
		.expect('Content-Type', /application\/json/)
		.expect(200, testMsg)
		.end(function(err, res) {
			if(err)
				throw err;
			console.log('** got the correct response **');
			kthxbye();
		});
});

