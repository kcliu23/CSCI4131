const http = require('http');
const url = require('url');
const fs = require('fs');

const port = 8006;  // last three digits DrDans x500id, change to yours!!!!

http.createServer(function(req,res){
	var q = url.parse(req.url,true);
	
	console.log("path: " + q.pathname);
	
	if (q.pathname === '/') {
		retIndexPage(req,res);
	}
	else if (q.pathname === '/index.html') {
		retIndexPage(req,res)
	}
	else if (q.pathname === '/JSONreqex.html') // ret file with ajax used to get locations.txt
	{
		retJSONreqex(req,res);
	}
	else if (q.pathname === '/FetchJsonLat.html') //ret file with Fetch used to get locations.txt
	{
		console.log("calling: retFetchJsonLat");
		retFetchJsonLat(req,res);
	}
	else if (q.pathname === '/FetchJsonTut.html') { // Route for FetchJsonTut.html
		retFetchJsonTut(req, res);
	} 
	// add code to call a function retFetchJsonTut here
	else if (q.pathname === '/locations.txt') {
		retLocations(req,res);
	}
	// add code to call a function retMyTutorials.txt here
	else if (q.pathname === '/myTutorials.txt') { // Route for myTutorials.txt
		retMyTutorials(req, res);
	}
	else {
		res.writeHead(404,{'Content-type':'text/html'});
		res.end("404 Not Found");
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

// returns file with Ajax that GETs locations.txt
function retJSONreqex(req,res) {
	fs.readFile('JSONreqex.html', (err, html) => {
		if (err) { throw err; }
		res.statusCode = 200;
		res.setHeader('Content-type', 'text/html');
		res.write(html);
		res.end();
	});
}

function retFetchJsonLat(req,res) { // returns file with Fetch get of locations.txt
	console.log("in retFetchJsonLat.html");
	fs.readFile('FetchJsonLat.html', (err, html) => {
		if (err) { throw err; }
		console.log("got file: ");
		// console.log(html);
		res.statusCode = 200;
		res.setHeader('Content-type', 'text/html');
		res.write(html);
		res.end();
	});
}

	// add  function retFetchJsonTut - which returns file FetchJsonTut.html here
function retFetchJsonTut(req, res) {
	fs.readFile('FetchJsonTut.html', (err, html) => {
		if (err) { throw err; }
		res.statusCode = 200;
		res.setHeader('Content-type', 'text/html');
		res.write(html);
		res.end();
	});
}
	// add  function retMyTutorials.txt - which returns file myTutorials.txt here

function retMyTutorials(req, res) {
	fs.readFile('myTutorials.txt', (err, text) => {
		if (err) { throw err; }
		res.statusCode = 200;
		res.setHeader('Content-type', 'text/plain');
		res.write(text);
		res.end();
	});
}
function retLocations(req,res) {  // returns the file locations.txt (has json string)
	fs.readFile('locations.txt', (err, text) => {
		if (err) { throw err; }
		let parsedJson = JSON.parse(text);
		res.statusCode = 200;
		res.setHeader('Content-type', 'application/json');
		res.write(JSON.stringify(parsedJson));
		res.end();
	});
}


