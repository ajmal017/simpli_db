import os
import json
import pickle
import typing
import asyncio
import requests
import aiohttp
import redis
import aioredis
import psycopg2
import asyncpg
import numba
import zstandard as zstd
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT')
RABBIT_URL = f'amqp://{RABBIT_HOST}:{RABBIT_PORT}//'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

REMOTE_REDIS_HOST = os.getenv('REMOTE_REDIS_HOST')
REMOTE_REDIS_PASS = os.getenv('REMOTE_REDIS_PASS')
REMOTE_REDIS_PORT = os.getenv('REMOTE_REDIS_PORT')
REMOTE_REDIS_URL = f'redis://:{REMOTE_REDIS_PASS}@{REMOTE_REDIS_HOST}:{REMOTE_REDIS_PORT}/0'

cctx = zstd.ZstdCompressor()
dctx = zstd.ZstdDecompressor()

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
remote_cache = redis.StrictRedis(host=REMOTE_REDIS_HOST, port=REMOTE_REDIS_PORT, password=REMOTE_REDIS_PASS)
db = psycopg2.connect(user=DB_USER, password=DB_PASS, database=DB_NAME, host=DB_HOST)



def compress(data):
    return cctx.compress(data)

def decompress(data):
    return dctx.decompress(data)

def to_json(data: pd.DataFrame):
    return data.to_json().encode('utf-8')

def from_json(raw):
    return pd.read_json(raw)

def to_numba(func: typing.Callable):
    return numba.jit()(func)



async def get_cache_conn():
    return await aioredis.create_redis_pool(REDIS_URL)

async def get_cache_data_async(key, conn):
    raw = await conn.get(key)
    return decompress(raw)

async def get_all_cache_data_async(*args):
    conn = await get_cache_conn()
    return await asyncio.gather(*(get_cache_data_async(key, conn) for key in args))



def get_cache_data(key):
    raw = cache.get(key)
    return decompress(raw)

def set_cache_data(key, data):
    cache.set(key, cctx.compress(json.dumps(data).encode('utf-8')))

def get_all_cache_data(*args):
    return tuple([get_cache_data(key) for key in args])



async def get_remote_cache_conn():
    return await aioredis.create_redis_pool(REMOTE_REDIS_URL)

async def get_all_remote_cache_data_async(*args):
    conn = await get_remote_cache_conn()
    return await asyncio.gather(*(get_cache_data_async(key, conn) for key in args))



def get_remote_cache_data(key):
    raw = remote_cache.get(key)
    return decompress(raw)

def set_remote_cache_data(key, data):
    remote_cache.set(key, cctx.compress(json.dumps(data).encode('utf-8')))

def get_all_remote_cache_data(*args):
    return tuple([get_remote_cache_data(key) for key in args])



async def get_db_conn():
    return await asyncpg.connect(user=DB_USER, password=DB_PASS, database=DB_NAME, host=DB_HOST)

async def read_sql_async(query: str, conn):
    stmt = await conn.prepare(query)
    columns = [rec.name for rec in stmt.get_attributes()]
    values = await conn.fetch(query)
    df = pd.DataFrame(values, columns=columns)
    return df

async def get_all_sql_data_async(*args):
    conn = await get_db_conn()
    return await asyncio.gather(*(read_sql_async(query, conn) for query in args))

def read_sql(query):
    return pd.read_sql(query, db)

def get_all_sql_data(*args):
    return tuple([read_sql(query) for query in args])

async def request_url_async(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def get_all_urls_async(*args):
    return await asyncio.gather(*(request_url_async(url) for url in args))

def request_url(url: str):
    return requests.get(url)

def get_all_urls(*args):
    return tuple([request_url(url) for url in args])