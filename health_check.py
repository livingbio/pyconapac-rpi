from lib import info
import requests
import logging
import time

api = 'http://codeme.krdai.info/api/machinelog/'

print info.MACHINE_ID, info.SD_ID

while True:
    try:
        r = requests.post(api, {
            'mid': info.MACHINE_ID
        })
        assert r.ok, r.text
    except Exception as e:
        logging.exception(e)

    # send signal every 1 mins
    time.sleep(60)
