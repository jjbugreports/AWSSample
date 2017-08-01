# AWSSample

## Link:
http://weathertest.us-east-1.elasticbeanstalk.com/

## AWS Components:

### Elastic Beanstalk - UI
 * Calls API and generates html.
 * Simple python app with wsgi.

### API Gateway - Expose API to python app in Elastic Beanstalk
 * Calls lambda function to gather and format data.

### Lambda
 * Gather's weather data from OpenWeatherMap API (https://openweathermap.org/)
 * Converts units from Kelvin to Fahrenheit.

### Other
 * Theme is a Twitter Bootstrap template from https://antjanus.com/blog/web-development-tutorials/front-end-development/customize-twitter-bootstrap-into-themes/)
