import datetime
import json
import logging
import logging.handlers

from urllib.request import urlopen
from wsgiref.simple_server import make_server


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/opt/python/log/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)



welcome = """
<html>
  <head>
    <title>Weather in Berkeley</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- <link href="http://getbootstrap.com/2.3.2/assets/css/bootstrap.css" rel="stylesheet" media="screen"> -->
    <link href="http://antjanus.github.io/Green-Bootstrap-Theme/newstrap.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
  </head>
<body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
         <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="#">Weather in Berkeley CA</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container"><h1>10 Day forecast</h1>%s</div></body></html>
"""

def new_welcome():
  # TODO: Move this to a config.
  api_url = 'https://tegjr5nhh0.execute-api.us-east-1.amazonaws.com/test/mydemoresource'
  try:
    response = urlopen(api_url)
  except Exception as e:
    logger.warning('Unable to access api.')
    logger.warning('%s'  % e)
    # TODO: Return error message
    return ''
  data = response.read()
  encoding = response.info().get_content_charset('utf-8')
  data = json.loads(data.decode(encoding))
  table = '<table class="table"><tr><th>Date</th><th>Low</th><th>High</th><th>Average (Sort key)</th></tr>{}</table>'
  table_str = ''
  start_date = datetime.date.today()
  temps = []
  for index, day_data in enumerate(data['list']):
    temps.append(((start_date + datetime.timedelta(days=index)), day_data['temp']['min'], day_data['temp']['max'], int((day_data['temp']['min'] + day_data['temp']['max']) / 2.0)))
  
  for date, mini, maxi, avg in sorted(temps, key=lambda x: -1*x[3]):  
    table_str += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td></tr>' % (date, mini, maxi, avg)

  return welcome % (table.format(table_str))



def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                logger.info("Received message: %s" % request_body)
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = new_welcome()
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
