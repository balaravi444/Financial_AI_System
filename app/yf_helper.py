# app/yf_helper.py
import time
import yfinance as yf
from curl_cffi import requests as cffi_requests

_cache = {}
CACHE_TTL = 300  # 5 min

# Browser-impersonating session — bypasses Yahoo's bot/IP blocking on cloud hosts
_session = cffi_requests.Session(impersonate="chrome")


def get_info_cached(symbol: str, retries: int = 3):
    """Fetch yf.Ticker(symbol).info with caching + retry/backoff for 429s."""
    now = time.time()
    if symbol in _cache and now - _cache[symbol]["time"] < CACHE_TTL:
        return _cache[symbol]["data"]

    last_err = None
    for i in range(retries):
        try:
            data = yf.Ticker(symbol, session=_session).info
            if data:
                _cache[symbol] = {"data": data, "time": now}
                return data
        except Exception as e:
            last_err = e
            if "429" in str(e) or "Too Many Requests" in str(e):
                time.sleep(2 ** i)  # 1s, 2s, 4s
                continue
            raise
    raise last_err or Exception("Failed to fetch data after retries")


def get_fast_info_cached(symbol: str, retries: int = 3):
    """Fetch yf.Ticker(symbol).fast_info with caching + retry/backoff for 429s."""
    cache_key = f"fast_{symbol}"
    now = time.time()
    if cache_key in _cache and now - _cache[cache_key]["time"] < CACHE_TTL:
        return _cache[cache_key]["data"]

    last_err = None
    for i in range(retries):
        try:
            fi = yf.Ticker(symbol, session=_session).fast_info
            _cache[cache_key] = {"data": fi, "time": now}
            return fi
        except Exception as e:
            last_err = e
            if "429" in str(e) or "Too Many Requests" in str(e):
                time.sleep(2 ** i)
                continue
            raise
    raise last_err or Exception("Failed to fetch data after retries")