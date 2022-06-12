"""
http://localhost:3000/dashboard/1-property-dashboard
"""
import os
import time

from dotenv import load_dotenv
import jwt


load_dotenv(dotenv_path=r'.env')
METABASE_SECRET_KEY = os.getenv('METABASE_SECRET_KEY')
METABASE_SITE_URL = 'http://localhost:3000'


if __name__ == '__main__':
    payload = {
        'resource': {'dashboard': 1},
        'params': {},
        'exp': round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm='HS256')

    iframe_url = f'{METABASE_SITE_URL}/embed/dashboard/{token}#theme=night&bordered=false&titled=true'

    print(iframe_url)
