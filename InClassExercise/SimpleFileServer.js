const http = require('http');
const url = require('url');
const fs = require('fs');

const port = 9001;

http.createServer(function(req,res){
	var q = url.parse(req.url,true);
	
	if (q.pathname === '/') {
		retIndexPage(req,res);
	}
	else if (q.pathname === '/index.html') {
		retIndexPage(req,res)
	}
	else {
		res.writeHead(404,{'Content-type':'text/html'});
		return res.end("404 Not Found");
	}
}).listen(port);

function retIndexPage(req,res) {
	fs.readFile('index.html', (err, html) => {
		if (err) { throw err; }
		res.statusCode = 200;
		res.setHeader('Content-type', 'text/html');
		res.write(html);
		res.end();
	});
}
