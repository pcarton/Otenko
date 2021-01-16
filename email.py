#!/usr/bin/python
import os, logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(level=LOG_LEVEL,format=FORMAT)

emailServer = os.environ.get('EMAIL_SERVER', 'unset server')
emailUsername = os.environ.get('EMAIL_USERNAME', 'unset username')
emailPassword = os.environ.get('EMAIL_PASSWORD', 'unset password')
woeid = os.environ.get('WOEID', 'unset woeid')
emailSenderAddress = os.environ.get('EMAIL_SENDER_ADDRESS', 'unset sender address')
emailRecipientAddress = os.environ.get('EMAIL_RECIPIENT_ADDRESS', 'unset recipient address')
openWeatherApiKey = os.environ.get('OPEN_WEATHER_API_KEY', 'unser open weather api key')
zipCode = os.environ.get('ZIPCODE', 'unset zipcode')
countryCode = os.environ.get('COUNTRY_CODE', 'unset countryCode')

logging.debug(f'EMAIL_SERVER:{emailServer}')
logging.debug(f'EMAIL_USERNAME:{emailUsername}')
logging.debug(f'WOEID:{woeid}')
logging.debug(f'EMAIL_SENDER_ADDRESS:{emailSenderAddress}')
logging.debug(f'EMAIL_RECIPIENT_ADDRESS:{emailRecipientAddress}')
logging.debug(f'ZIPCODE:{zipCode}')
logging.debug(f'COUNTRY_CODE:{countryCode}')