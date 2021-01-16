#!/usr/bin/python3.1

serverName = os.environ.get('EMAIL_SERVER', 'unset')
username = os.environ.get('EMAIL_USERNAME', 'unset')
password = os.environ.get('EMAIL_PASSWORD', 'unset')
woeid = os.environ.get('WOEID', 'unset')
fromaddr = os.environ.get('EMAIL_SENDER_ADDRESS', 'unset')
toaddr = os.environ.get('EMAIL_RECIPIENT_ADDRESS', 'unset')
weatherAPI = os.environ.get('OPEN_WEATHER_API_KEY', 'unset')
zipCode = os.environ.get('ZIPCODE', 'unset')
countryCode = os.environ.get('COUNTRY_CODE', 'unset')

print(f'EMAIL_SERVER:{EMAIL_SERVER}')