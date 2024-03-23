from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus, quote,urlencode
import re
import stat
import glob
import os
import datetime
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
    Url, *_ = url.split("?", 1)
    # Define a dictionary to map file extensions to MIME types
    mime_types = {
        "html": "text/html",
        "css": "text/css",
        "js": "text/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "mp3": "audio/mpeg",
        "txt": "text/plain",
    }

    file_extension = url.split(".")[-1]
    Url = Url.split("/")[-1]
    file_path = find_file_full_path(os.getcwd(),"",Url)
    
    if Url == "redirect":
        query = url.split("?")[1]
        query_params = dict(q.split("=") for q in query.split("&"))
        redirect_url = f"{unquote_plus(query_params['website'])}{unquote_plus(query_params['query'])}"
        return  "",307,redirect_url
    if Url == "calculator":
        query = unquote_plus(url.split('?')[1])
        query_params = dict(q.split("=") for q in query.split("&"))
        print(query_params)
        try:
            num1 = float(query_params["number1"])
            operator = query_params["operator"]
            num2 = float(query_params["number2"])
        except (KeyError, ValueError):
            return "Invalid request", 400, "text/plain"

        result = None
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                return "Cannot divide by zero", 400, "text/plain"
            result = num1 / num2

        return str(result), 200, "text/plain"
    if Url == "files":
        dir_path = find_file_full_path(os.getcwd(),Url,"")
        file_types = (".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".mp3", ".txt")
        files = []
        
        for file_type in file_types:
            files.extend(glob.glob(f"{dir_path}/*{file_type}"))

        if not files:
            return "No supported files found", 404, "text/plain"

        table_rows = "".join(f"<tr><td><a href='/files/{file}'>{file}</a></td></tr>" for file in files)
        table_html = f"<tbody>{table_rows}</tbody>"
        
        with open(find_file_full_path(os.getcwd(),"","explorer.html"), 'r') as f:
            Content = f.read()
            
        insert_at_index = Content.index('<!-- Insert code here -->')
        
        insert_before = Content[:insert_at_index]
        insert_after = Content[insert_at_index:]
        
        return insert_before+table_html+insert_after, 200, "text/html"
    
    if file_extension in mime_types:
        content_type = mime_types[file_extension]
    
        file_mode = "r" if content_type.startswith("text") else "rb"

        try:
            if Url == "EventLog.html":
                table_content = ""
                days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                with open(find_file_full_path(os.getcwd(),"","eventlogTemplate.html"), 'r') as f:
                    eventContent = f.read()
                if(body==None and len(submissions)==0):
                    with open(file_path, "w") as file:
                        file.write(eventContent)
                if(body!=None):
                    parameters = get_body_params(body)
                    submissions.append(parameters)
                    submissions_sorted = sorted(submissions, key=lambda x: days_order.index(x['day']))
                    for submission in submissions_sorted:
                        table_content += submission_to_table(get_body_params(submission))
                        
                    insert_at_index = eventContent.index('<!-- Insert code here -->')
                    
                    insert_before = eventContent[:insert_at_index]
                    insert_after = eventContent[insert_at_index:]
                    eventContent = insert_before + table_content + insert_after
                    
                    with open(file_path, "w") as file:
                        file.write(eventContent)
            
            if int(oct(os.stat(file_path).st_mode)[-3:]) <= 640:
                raise PermissionError
            else:
                with open(file_path, file_mode) as file:
                    file_content = file.read()
                    return file_content,200, content_type
        except FileNotFoundError:
            return open(find_file_full_path(os.getcwd(),"","404.html")).read(),404, content_type
        except PermissionError:
            return open(find_file_full_path(os.getcwd(),"","403.html")).read(),403,content_type
        
        
    return open(find_file_full_path(os.getcwd(),"","404.html")).read(),404, "text/html"

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
        response_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_status = response_code
        response_headers =headers
        with open("response.log", "a") as response_log:
            response_log.write(f"{response_time} - {response_status} - {response_headers} {self.path}\n")

    def do_GET(self):
        # Call the student-edited server code.
        message,status,content_type = handle_req(self.path)
        # Convert the return value into a byte string for network transmission
        if status == 307:  # Check if redirection is needed
            self.send_response(status)
            self.send_header("Location", content_type)  # Set the Location header
            self.end_headers()
        else:
            if type(message) == str:
                message = bytes(message, "utf8")

            self.__c_send_response(
                message,
                status,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )

    def do_POST(self):
        body = self.__c_read_body()
        message,status, content_type = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            status,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )
        
def find_file_full_path(root_dir, dir_name,file_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == file_name:
                return os.path.join(dirpath, filename)
        for dirname in dirnames:
            if dirname == dir_name:
                return os.path.join(dirpath, dirname)
    return None

def run():
    PORT = 8080
    print(f"Starting server http://localhost:{PORT}/MySchedule.html")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
