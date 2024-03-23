from http.server import BaseHTTPRequestHandler, HTTPServer
import os
def getFile(url):
    """
    The url parameter is a *PARTIAL* URL of type string that contains
    the path name and query string.
    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe"

    This function should return a string.
    """
    # Find the index of ? and/or # and ignore everything after it
    url = url.split('?', 1)[0].split('#', 1)[0]

    # Determine file path based on URL
    base_path = "/Users/kaichengliu/Desktop/exchange_program/springsemester/csci4131/assignment1/"
    file_path = url
    print(base_path+file_path[1:])

    # Check if the file exists
    # if os.path.exists(file_path):
        # Check file extension to determine content type
    file, file_extension = os.path.splitext(file_path)
    print(file)
    print(file_extension.lower())
    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        with open(base_path+file_path[1:], 'rb') as img_file:
            return img_file.read()
    else:
        if file.startswith("/My"):
            return open("/Users/kaichengliu/Desktop/exchange_program/springsemester/csci4131/assignment1/MySchedule.html").read()
        elif file.startswith("/Ab"):
            return open("/Users/kaichengliu/Desktop/exchange_program/springsemester/csci4131/assignment1/AboutMe.html").read()
        else:
            return open("/Users/kaichengliu/Desktop/exchange_program/springsemester/csci4131/assignment1/404.html").read()
   
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message = getFile(self.path)
        if self.path.endswith(('.JPG', '.jpeg')):
            content_type = "image/jpeg"
        else:
            content_type = "text/html; charset=utf-8"
        
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
