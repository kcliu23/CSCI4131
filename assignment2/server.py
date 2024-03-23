from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
import re

submissions = []

def get_body_params(body):
    if not body:
        return {}
    if isinstance(body, dict):
        return body
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict


def submission_to_table(item):
    """TODO: Takes a dictionary of form parameters and returns an HTML table row

    An example input dictionary might look like: 
    {
     'event': 'Sleep',
     'day': 'Sun',
     'start': '01:00',
     'end': '11:00', 
     'phone': '1234567890', 
     'location': 'Home',
     'extra': 'Have a nice dream', 
    }
    """
    event_name = item.get('event', '')
    day = item.get('day', '')
    start_time = item.get('start', '')
    stop_time = item.get('end', '')
    phone_number = item.get('phone', '')
    location = item.get('location', '')
    extra_info = item.get('extra', '')
    url = item.get('url', '')
    # print("Event Name:", event_name)
    if not re.match("^[a-zA-Z0-9 ]+$", event_name):
        return "<tr><td colspan='8'>Error: Event Name should contain only alphanumeric characters and spaces.</td></tr>"
    table_row = f"""
        <tr>
            <td>{event_name}</td>
            <td>{day}</td>
            <td>{start_time}</td>
            <td>{stop_time}</td>
            <td>{phone_number}</td>
            <td>{location}</td>
            <td>{extra_info}</td>
            <td><a href="{url}">{url}</a></td>
        </tr>
    """
    return table_row

# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
def handle_req(url, body=None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/MyForm.html?name=joe` then the `url` parameter will have
    the value "/MyForm.html?name=joe"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """

    # Get rid of any query string parameters
    url, *_ = url.split("?", 1)
    # Parse any form parameters submitted via POST
    # parameters = get_body_params(body)
    if url == "/MySchedule.html":
        return open("./static/html/MySchedule.html").read(), "text/html"
    if url == "/MyForm.html":
        return open("./static/html/MyForm.html").read(), "text/html"
    elif url == "/AboutMe.html":
        return open("./static/html/AboutMe.html").read(), "text/html"
    elif url == "/img/gophers-mascot.png":
        return open("./static/img/gophers-mascot.png", "rb").read(), "image/png"
    # NOTE: These files may be different for your server, but we include them to
    # show you examples of how yours may look. You may need to change the paths
    # to match the files you want to serve. Before you do that, make sure you
    # understand what the code is doing, specifically with the MIME types and
    # opening some files in binary mode, i.e. `open(..., "br")`.
    elif url == "/css/style.css":
        return open("./static/css/style.css").read(), "text/css"
    elif url == "/js/thumbnail.js":
        return open("./static/js/thumbnail.js").read(), "text/javascript"
    elif url == "/js/clock.js":
        return open("./static/js/clock.js").read(), "text/javascript"
    elif url == "/img/zoom.jpg":
        return open("./static/img/zoom.jpg", "br").read(), "image/jpeg"
    elif url == "/img/IMG_6917.jpg":
        return open("./static/img/IMG_6917.jpg", "rb").read(), "image/jpeg"
    elif url == "/img/rec.jpg":
        return open("./static/img/rec.jpg", "br").read(), "image/jpeg"
    elif url == "/img/anderson.jpg":
        return open("./static/img/anderson.jpg", "br").read(), "image/jpeg"
    elif url == "/img/folwel.jpg":
        return open("./static/img/folwel.jpg", "br").read(), "image/jpeg"
    # TODO: Add update the HTML below to match your other pages and
    # implement the `submission_to_table`.
    elif url == "/EventLog.html":
        file_path = "./static/html/EventLog.html"
        table_content = ""
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        if(body==None and len(submissions)==0):
            eventContent = """
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <title> Event Submission </title>
                        <meta name="viewport" content="width=device-width">
                        <meta charset="UTF-8">
                        <link rel="stylesheet" href="../css/style.css">
                    </head>
                    <body>
                        <nav>
                            <ul>
                                <li><a href="/MySchedule.html">My Schedule</a></li>
                                <li><a href="/MyForm.html">Form Input</a></li>
                                <li><a href="/AboutMe.html">About Me</a></li>
                                <li><a href="/EventLog.html">Event History</a></li>
                            </ul>
                        </nav>
                        <h1> My New Events </h1>
                        <div class = "container">
                            <table class="schedule-table">
                                <tr>
                                    <th>Event</th>
                                    <th>Day</th>
                                    <th>Start</th>
                                    <th>End</th>
                                    <th>Phone</th>
                                    <th>Location</th>
                                    <th>Extra Info</th>
                                    <th>URL</th>
                                </tr>
                            </table>
                            <div id="large-image-container">
                            </div>
                        </div>
                    </body>
                    </html>
                    """
            with open(file_path, "w") as file:
                file.write(eventContent)
        if(body!=None):
            parameters = get_body_params(body)
            submissions.append(parameters)
            submissions_sorted = sorted(submissions, key=lambda x: days_order.index(x['day']))
            for submission in submissions_sorted:
                table_content += submission_to_table(get_body_params(submission))
            eventContent = """
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <title> Event Submission </title>
                        <meta name="viewport" content="width=device-width">
                        <meta charset="UTF-8">
                        <link rel="stylesheet" href="../css/style.css">
                    </head>
                    <body>
                        <nav>
                            <ul>
                                <li><a href="/MySchedule.html">My Schedule</a></li>
                                <li><a href="/MyForm.html">Form Input</a></li>
                                <li><a href="/AboutMe.html">About Me</a></li>
                                <li><a href="/EventLog.html">Event History</a></li>
                            </ul>
                        </nav>
                        <h1> My New Events </h1>
                        <div class = "container">
                            <table class="schedule-table">
                                <tr>
                                    <th>Event</th>
                                    <th>Day</th>
                                    <th>Start</th>
                                    <th>End</th>
                                    <th>Phone</th>
                                    <th>Location</th>
                                    <th>Extra Info</th>
                                    <th>URL</th>
                                </tr>
                                """+ table_content+"""
                            </table>
                            <div id="large-image-container">
                            </div>
                        </div>
                    </body>
                    </html>
                    """
            with open(file_path, "w") as file:
                file.write(eventContent)
        
        return open("./static/html/EventLog.html").read(), "text/html; charset=utf-8"
    else:
        return open("./static/html/404.html").read(), "text/html; charset=utf-8"


# You shouldn't change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body

    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = handle_req(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )

    def do_POST(self):
        body = self.__c_read_body()
        message, content_type = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
