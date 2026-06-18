# app/stock_analyzer.py
import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands
from datetime import datetime
import time

NSE_SUFFIX = ".NS"
BSE_SUFFIX = ".BO"

INDEX_MAP = {
    "NIFTY":       "^NSEI",
    "NIFTY50":     "^NSEI",
    "BANKNIFTY":   "^NSEBANK",
    "SENSEX":      "^BSESN",
    "NIFTYIT":     "^CNXIT",
}


def get_stock_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        return symbol
    if symbol in INDEX_MAP:
        return INDEX_MAP[symbol]
    if symbol.startswith("^"):
        return symbol
    return symbol + NSE_SUFFIX


def fetch_stock_data(symbol: str, period: str = "3mo"):
    symbol = symbol.upper().strip()

    # Resolve index
    if symbol in INDEX_MAP:
        sym = INDEX_MAP[symbol]
        try:
            df = yf.Ticker(sym).history(period=period)
            if not df.empty and len(df) > 5:
                return df, sym
        except Exception:
            pass
        return pd.DataFrame(), sym

    # Already has suffix
    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        try:
            df = yf.Ticker(symbol).history(period=period)
            if not df.empty and len(df) > 5:
                return df, symbol
        except Exception:
            pass
        return pd.DataFrame(), symbol

    # Try NSE first then BSE
    for suffix in [NSE_SUFFIX, BSE_SUFFIX]:
        sym = symbol + suffix
        try:
            df = yf.Ticker(sym).history(period=period)
            if not df.empty and len(df) > 5:
                return df, sym
        except Exception:
            time.sleep(0.3)
            continue

    return pd.DataFrame(), symbol + NSE_SUFFIX


def get_stock_info(symbol: str):
    symbol = symbol.upper().strip()

    if symbol in INDEX_MAP:
        sym = INDEX_MAP[symbol]
        try:
            return yf.Ticker(sym).info, sym
        except Exception:
            return {}, sym

    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        try:
            info = yf.Ticker(symbol).info
            if info.get("longName") or info.get("shortName"):
                return info, symbol
        except Exception:
            pass
        return {}, symbol

    for suffix in [NSE_SUFFIX, BSE_SUFFIX]:
        sym = symbol + suffix
        try:
            info = yf.Ticker(sym).info
            if info.get("longName") or info.get("shortName"):
                return info, sym
        except Exception:
            continue

    return {}, symbol + NSE_SUFFIX


def calculate_indicators(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 20:
        return {}

    close = df["Close"]
    high  = df["High"]
    low   = df["Low"]

    # RSI
    rsi       = RSIIndicator(close=close, window=14)
    rsi_value = round(float(rsi.rsi().iloc[-1]), 2)

    # MACD
    macd        = MACD(close=close)
    macd_value  = round(float(macd.macd().iloc[-1]), 2)
    macd_signal = round(float(macd.macd_signal().iloc[-1]), 2)
    macd_diff   = round(float(macd.macd_diff().iloc[-1]), 2)

    # Moving Averages
    sma20_value = round(float(SMAIndicator(close=close, window=20).sma_indicator().iloc[-1]), 2)
    sma50_value = round(float(SMAIndicator(close=close, window=50).sma_indicator().iloc[-1])
                        if len(df) >= 50 else 0, 2)
    ema20_value = round(float(EMAIndicator(close=close, window=20).ema_indicator().iloc[-1]), 2)

    # Bollinger Bands
    bb          = BollingerBands(close=close, window=20)
    bb_upper    = round(float(bb.bollinger_hband().iloc[-1]), 2)
    bb_lower    = round(float(bb.bollinger_lband().iloc[-1]), 2)
    bb_mid      = round(float(bb.bollinger_mavg().iloc[-1]), 2)

    # Price data
    current_price = round(float(close.iloc[-1]), 2)
    prev_price    = round(float(close.iloc[-2]), 2)
    price_change  = round(current_price - prev_price, 2)
    pct_change    = round((price_change / prev_price) * 100, 2)

    # 52 week
    week52_high = round(float(close.rolling(window=min(252, len(close))).max().iloc[-1]), 2)
    week52_low  = round(float(close.rolling(window=min(252, len(close))).min().iloc[-1]), 2)

    # Volume
    avg_volume     = int(df["Volume"].rolling(window=20).mean().iloc[-1])
    current_volume = int(df["Volume"].iloc[-1])

    return {
        "current_price":  current_price,
        "prev_price":     prev_price,
        "price_change":   price_change,
        "pct_change":     pct_change,
        "week52_high":    week52_high,
        "week52_low":     week52_low,
        "rsi":            rsi_value,
        "macd":           macd_value,
        "macd_signal":    macd_signal,
        "macd_diff":      macd_diff,
        "sma_20":         sma20_value,
        "sma_50":         sma50_value,
        "ema_20":         ema20_value,
        "bb_upper":       bb_upper,
        "bb_lower":       bb_lower,
        "bb_mid":         bb_mid,
        "avg_volume":     avg_volume,
        "current_volume": current_volume
    }


def interpret_indicators(indicators: dict) -> dict:
    signals = []
    score   = 0

    rsi = indicators.get("rsi", 50)
    if rsi < 30:
        signals.append("RSI is OVERSOLD (below 30) — possible buying opportunity")
        score += 2
    elif rsi < 45:
        signals.append("RSI is WEAK — stock losing momentum")
        score += 1
    elif rsi > 70:
        signals.append("RSI is OVERBOUGHT (above 70) — caution, possible pullback")
        score -= 2
    elif rsi > 55:
        signals.append("RSI is STRONG — good momentum")
        score += 1

    macd   = indicators.get("macd", 0)
    signal = indicators.get("macd_signal", 0)
    if macd > signal:
        signals.append("MACD crossed ABOVE signal line — bullish signal")
        score += 2
    else:
        signals.append("MACD is BELOW signal line — bearish signal")
        score -= 1

    price = indicators.get("current_price", 0)
    sma20 = indicators.get("sma_20", 0)
    sma50 = indicators.get("sma_50", 0)
    if price > sma20 > sma50:
        signals.append("Price ABOVE both SMA20 and SMA50 — strong uptrend")
        score += 2
    elif price > sma20:
        signals.append("Price ABOVE SMA20 — short-term bullish")
        score += 1
    elif price < sma20 < sma50:
        signals.append("Price BELOW both moving averages — downtrend")
        score -= 2

    bb_upper = indicators.get("bb_upper", 0)
    bb_lower = indicators.get("bb_lower", 0)
    if price >= bb_upper:
        signals.append("Price near UPPER Bollinger Band — overbought zone")
        score -= 1
    elif price <= bb_lower:
        signals.append("Price near LOWER Bollinger Band — oversold zone")
        score += 1

    if score >= 4:
        recommendation = "STRONG BUY"
    elif score >= 2:
        recommendation = "BUY"
    elif score <= -3:
        recommendation = "STRONG SELL"
    elif score <= -1:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    return {
        "signals":        signals,
        "score":          score,
        "recommendation": recommendation
    }


def calculate_targets(indicators: dict) -> dict:
    price    = indicators.get("current_price", 0)
    bb_upper = indicators.get("bb_upper", price * 1.05)
    bb_lower = indicators.get("bb_lower", price * 0.95)
    sma20    = indicators.get("sma_20", price)

    stop_loss     = round(price * 0.95, 2)
    target_1      = round(min(bb_upper, price * 1.05), 2)
    target_2      = round(price * 1.10, 2)
    support_level = round(max(bb_lower, sma20 * 0.98), 2)
    risk_reward   = round((target_1 - price) / (price - stop_loss), 2) \
                    if price != stop_loss else 0

    return {
        "entry_price":   price,
        "stop_loss":     stop_loss,
        "target_1":      target_1,
        "target_2":      target_2,
        "support_level": support_level,
        "risk_reward":   risk_reward
    }


def full_stock_analysis(symbol: str) -> dict:
    try:
        df, actual_sym = fetch_stock_data(symbol)
        info, _        = get_stock_info(symbol)

        if df.empty:
            return {
                "error": (
                    f"Could not find '{symbol}' on NSE or BSE. "
                    f"Try the exact NSE symbol e.g. RELIANCE, TCS, INFY, HDFCBANK. "
                    f"For BSE-only stocks add .BO e.g. BAJAJFINSV.BO"
                )
            }

        indicators     = calculate_indicators(df)
        interpretation = interpret_indicators(indicators)
        targets        = calculate_targets(indicators)

        company_name = info.get("longName") or info.get("shortName") or symbol
        sector       = info.get("sector",   "Unknown")
        industry     = info.get("industry", "Unknown")
        market_cap   = info.get("marketCap", 0)
        pe_ratio     = info.get("trailingPE", 0)
        pb_ratio     = info.get("priceToBook", 0)
        dividend     = info.get("dividendYield", 0)

        clean_symbol = actual_sym.replace(".NS", "").replace(".BO", "")

        return {
            "symbol":         clean_symbol,
            "full_symbol":    actual_sym,
            "company_name":   company_name,
            "sector":         sector,
            "industry":       industry,
            "market_cap":     market_cap,
            "pe_ratio":       round(pe_ratio, 2) if pe_ratio else "N/A",
            "pb_ratio":       round(pb_ratio, 2) if pb_ratio else "N/A",
            "dividend":       round(dividend * 100, 2) if dividend else 0,
            "indicators":     indicators,
            "current_price":  indicators.get("current_price", 0),
            "pct_change":     indicators.get("pct_change", 0),
            "signals":        interpretation["signals"],
            "score":          interpretation["score"],
            "recommendation": interpretation["recommendation"],
            "targets":        targets,
            "analysis_time":  datetime.now().strftime("%d %b %Y %I:%M %p")
        }

    except Exception as e:
        return {"error": str(e)}


def format_analysis_for_ai(analysis: dict) -> str:
    if "error" in analysis:
        return f"Stock analysis error: {analysis['error']}"

    ind = analysis["indicators"]
    tgt = analysis["targets"]

    return f"""
LIVE STOCK ANALYSIS — {analysis['company_name']} ({analysis['symbol']}):

PRICE DATA:
- Current Price: ₹{ind['current_price']}
- Change Today:  ₹{ind['price_change']} ({ind['pct_change']}%)
- 52 Week High:  ₹{ind['week52_high']}
- 52 Week Low:   ₹{ind['week52_low']}

FUNDAMENTALS:
- Sector: {analysis['sector']}
- Market Cap: ₹{analysis['market_cap']:,}
- P/E Ratio: {analysis['pe_ratio']}
- P/B Ratio: {analysis['pb_ratio']}
- Dividend Yield: {analysis['dividend']}%

TECHNICAL INDICATORS:
- RSI (14): {ind['rsi']}
- MACD: {ind['macd']} | Signal: {ind['macd_signal']}
- SMA 20: ₹{ind['sma_20']} | SMA 50: ₹{ind['sma_50']}
- Bollinger Upper: ₹{ind['bb_upper']} | Lower: ₹{ind['bb_lower']}

SIGNALS:
{chr(10).join(f'- {s}' for s in analysis['signals'])}

SCORE: {analysis['score']}/7
RECOMMENDATION: {analysis['recommendation']}

TRADE LEVELS:
- Entry:      ₹{tgt['entry_price']}
- Stop Loss:  ₹{tgt['stop_loss']}
- Target 1:   ₹{tgt['target_1']}
- Target 2:   ₹{tgt['target_2']}
- Risk/Reward:{tgt['risk_reward']}

Based on this LIVE data, provide:
1. Technical analysis in simple words
2. Buy/sell/hold reasoning
3. Risk warning
4. SEBI disclaimer
""".strip()