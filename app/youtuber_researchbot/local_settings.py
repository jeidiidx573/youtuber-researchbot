

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'gfj5pw8s&^v1us1v7+npa3&w0_pvsj&jevd8fqf@0+zt$eg#so'
ACCESS_TOKEN = '5EdpCflALcAFsRaJMKCnAby9aeA3s2l/btCg1451QwQmWfzKyOc726veaYhM0gHv4qb+7G8vz8VwMTUHORDgP6m9qveWwJABn+SN+5rLpE8ZAy1/D+bBx4eWPLcmvSmttxHSY/0SPuWO/NRNZV6+5wdB04t89/1O/w1cDnyilFU='
DEVELOPER_KEY = "AIzaSyA25r9qCpM7ZPCw3_D8M7XcocSGFW-m-sk"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
