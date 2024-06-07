import pytz
from wsgiref.simple_server import make_server
import json
import datetime

def get_request_handler(path):
    tz_name = path.strip('/') or 'GMT'
    try:
        tz = pytz.timezone(tz_name)
        current_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        response_body = f'''
            <html>
            <head></head>
            <body>
            {current_time}
            </body>
            </html>
        '''
        headers = [('Content-Type', 'text/html')]
        return response_body, headers, 200
    except pytz.UnknownTimeZoneError:
        return error_handler('Unknown time zone', 400)
    except Exception as e:
        return error_handler(f'Internal server error: {str(e)}', 500)

def post_convert_handler(data, path):
    try:
        date_time_str = data['date']
        source_tz_name = data['tz']
        target_tz_name = path.strip('/api/v1/convert/')
        
        source_tz = pytz.timezone(source_tz_name)
        target_tz = pytz.timezone(target_tz_name)
        date_time = datetime.datetime.strptime(date_time_str, '%m.%d.%Y %H:%M:%S').replace(tzinfo=source_tz)
        converted_date_time = date_time.astimezone(target_tz)
        
        headers = [('Content-Type', 'application/json')]
        response_body = json.dumps({'converted_time': converted_date_time.strftime('%Y-%m-%d %H:%M:%S %Z')})
        return response_body, headers, 200
    except (KeyError, ValueError):
        return error_handler('Invalid input data', 400)
    except pytz.UnknownTimeZoneError:
        return error_handler('Unknown time zone', 400)
    except Exception as e:
        return error_handler(f'Internal server error: {str(e)}', 500)

def post_datediff_handler(data, path):
    try:
        first_date_time_str = data['first_date']
        first_tz_name = data['first_tz']
        second_date_time_str = data['second_date']
        second_tz_name = data['second_tz']
        
        first_tz = pytz.timezone(first_tz_name)
        second_tz = pytz.timezone(second_tz_name)
        first_date_time = datetime.datetime.strptime(first_date_time_str, '%d.%m.%Y %H:%M:%S').replace(tzinfo=first_tz)
        second_date_time = datetime.datetime.strptime(second_date_time_str, '%I:%M%p %Y-%m-%d').replace(tzinfo=second_tz)
        
        time_difference = (first_date_time - second_date_time).total_seconds()
        headers = [('Content-Type', 'application/json')]
        response_body = json.dumps({'time_difference_seconds': time_difference})
        return response_body, headers, 200
    except (KeyError, ValueError):
        return error_handler('Invalid input data', 400)
    except pytz.UnknownTimeZoneError:
        return error_handler('Unknown time zone', 400)
    except Exception as e:
        return error_handler(f'Internal server error: {str(e)}', 500)

def app(environ, response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    
    if method == 'GET':
        response_body, headers, status_code = get_request_handler(path)
    elif method == 'POST' and '/api/v1/convert' in path:
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        data = json.loads(request_body)
        response_body, headers, status_code = post_convert_handler(data, path)
    elif method == 'POST' and path == '/api/v1/datediff':
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        data = json.loads(request_body)
        response_body, headers, status_code = post_datediff_handler(data, path)
    else:
        response_body, headers, status_code = error_handler('Unknown request', 404)

    response(f'{status_code} {"OK" if status_code == 200 else "ERROR"}', headers)
    return [response_body.encode('utf-8')]

def error_handler(message, status_code):
    headers = [('Content-Type', 'text/html')]
    response_body = f'''
        <html>
        <head></head>
        <body>
        <h1>Error {status_code}</h1>
        <p>{message}</p>
        </body>
        </html>
    '''
    return response_body, headers, status_code

if __name__ == '__main__':
    port_address = 4900
    with make_server('', port_address, app) as httpd:
        print(f"Starting on port: {port_address}")
        httpd.serve_forever()
