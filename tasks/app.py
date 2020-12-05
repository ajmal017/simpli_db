"""
Celery 실행 방법:

celery -A tasks worker --loglevel=INFO --concurrency=1 -n worker1@%h
"""
import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT')
RABBIT_URL = f'amqp://{RABBIT_HOST}:{RABBIT_PORT}//'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

app = Celery('tasks', broker=RABBIT_URL, backend=REDIS_URL)