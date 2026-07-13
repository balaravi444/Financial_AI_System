# app/yf_helper.py
import time
import yfinance as yf
from curl_cffi import requests as cffi_requests

_cache = {}
CACHE_TTL = 300  # 5 min

# Browser-impersonating session — bypasses Yahoo's bot/IP blocking on cloud hosts
_session = cffi_requests.Session(impersonate="chrome")


def get_info_cached(symbol: str, retries: int = 3):
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
                time.sleep(2 ** i)
                continue
            raise
    raise last_err or Exception("Failed to fetch data after retries")


def get_fast_info_cached(symbol: str, retries: int = 3):
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


def get_history_cached(symbol: str, period: str = "3mo", retries: int = 3):
    cache_key = f"hist_{symbol}_{period}"
    now = time.time()
    if cache_key in _cache and now - _cache[cache_key]["time"] < CACHE_TTL:
        return _cache[cache_key]["data"]

    last_err = None
    for i in range(retries):
        try:
            df = yf.Ticker(symbol, session=_session).history(period=period)
            if not df.empty:
                _cache[cache_key] = {"data": df, "time": now}
                return df
        except Exception as e:
            last_err = e
            if "429" in str(e) or "Too Many Requests" in str(e):
                time.sleep(2 ** i)
                continue
            raise
    raise last_err or Exception("Failed to fetch history after retries")