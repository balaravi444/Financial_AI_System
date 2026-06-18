# app/db_manager.py
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "financeai.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c    = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        session_id   TEXT PRIMARY KEY,
        name         TEXT,
        age          INTEGER,
        monthly_income    REAL,
        monthly_expenses  REAL,
        risk_tolerance    TEXT DEFAULT 'medium',
        financial_goals   TEXT DEFAULT 'not specified',
        existing_investments TEXT DEFAULT 'none',
        has_insurance     INTEGER DEFAULT 0,
        dependents        INTEGER DEFAULT 0,
        debts             TEXT DEFAULT 'none',
        created_at        TEXT,
        updated_at        TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role       TEXT,
        content    TEXT,
        timestamp  TEXT,
        FOREIGN KEY (session_id) REFERENCES profiles(session_id)
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS financial_snapshots (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id      TEXT,
        month           TEXT,
        income          REAL,
        expenses        REAL,
        savings         REAL,
        savings_rate    REAL,
        health_score    INTEGER,
        timestamp       TEXT,
        FOREIGN KEY (session_id) REFERENCES profiles(session_id)
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id  TEXT,
        title       TEXT,
        target_amount REAL,
        saved_amount  REAL DEFAULT 0,
        deadline    TEXT,
        status      TEXT DEFAULT 'active',
        created_at  TEXT,
        FOREIGN KEY (session_id) REFERENCES profiles(session_id)
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id  TEXT,
        asset_type  TEXT,
        asset_name  TEXT,
        invested    REAL,
        current_value REAL,
        monthly_sip   REAL DEFAULT 0,
        start_date  TEXT,
        FOREIGN KEY (session_id) REFERENCES profiles(session_id)
    )""")

    conn.commit()
    conn.close()

def save_profile(session_id: str, data: dict):
    conn = get_connection()
    c    = conn.cursor()
    now  = datetime.now().isoformat()

    c.execute("""
    INSERT INTO profiles (
        session_id, name, age, monthly_income, monthly_expenses,
        risk_tolerance, financial_goals, existing_investments,
        has_insurance, dependents, debts, created_at, updated_at
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(session_id) DO UPDATE SET
        name=excluded.name, age=excluded.age,
        monthly_income=excluded.monthly_income,
        monthly_expenses=excluded.monthly_expenses,
        risk_tolerance=excluded.risk_tolerance,
        financial_goals=excluded.financial_goals,
        existing_investments=excluded.existing_investments,
        has_insurance=excluded.has_insurance,
        dependents=excluded.dependents,
        debts=excluded.debts,
        updated_at=excluded.updated_at
    """, (
        session_id,
        data.get("name"),
        data.get("age"),
        data.get("monthly_income"),
        data.get("monthly_expenses"),
        data.get("risk_tolerance", "medium"),
        data.get("financial_goals", "not specified"),
        data.get("existing_investments", "none"),
        1 if data.get("has_insurance") else 0,
        data.get("dependents", 0),
        data.get("debts", "none"),
        now, now
    ))
    conn.commit()
    conn.close()

def get_profile(session_id: str) -> dict | None:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE session_id=?", (session_id,))
    row  = c.fetchone()
    conn.close()

    if not row:
        return None

    d = dict(row)
    d["has_insurance"] = bool(d["has_insurance"])
    return d

def save_message(session_id: str, role: str, content: str):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    INSERT INTO conversations (session_id, role, content, timestamp)
    VALUES (?,?,?,?)
    """, (session_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_conversation_history(session_id: str, limit: int = 20) -> list:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    SELECT role, content FROM conversations
    WHERE session_id=?
    ORDER BY id DESC LIMIT ?
    """, (session_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

def save_snapshot(session_id: str, profile: dict, health_score: int):
    conn  = get_connection()
    c     = conn.cursor()
    month = datetime.now().strftime("%Y-%m")
    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    savings  = income - expenses
    rate     = round((savings / income * 100), 1) if income > 0 else 0

    c.execute("""
    INSERT OR REPLACE INTO financial_snapshots
    (session_id, month, income, expenses, savings, savings_rate, health_score, timestamp)
    VALUES (?,?,?,?,?,?,?,?)
    """, (session_id, month, income, expenses, savings, rate,
          health_score, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_snapshots(session_id: str, months: int = 6) -> list:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    SELECT month, income, expenses, savings, savings_rate, health_score
    FROM financial_snapshots
    WHERE session_id=?
    ORDER BY month DESC LIMIT ?
    """, (session_id, months))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def add_goal(session_id: str, title: str,
             target: float, deadline: str) -> int:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    INSERT INTO goals (session_id, title, target_amount, deadline, created_at)
    VALUES (?,?,?,?,?)
    """, (session_id, title, target, deadline, datetime.now().isoformat()))
    goal_id = c.lastrowid
    conn.commit()
    conn.close()
    return goal_id

def update_goal(goal_id: int, saved_amount: float):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    UPDATE goals SET saved_amount=?,
    status = CASE WHEN saved_amount >= target_amount THEN 'completed' ELSE 'active' END
    WHERE id=?
    """, (saved_amount, goal_id))
    conn.commit()
    conn.close()

def get_goals(session_id: str) -> list:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    SELECT * FROM goals WHERE session_id=? ORDER BY created_at DESC
    """, (session_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_portfolio_item(session_id: str, asset_type: str,
                       asset_name: str, invested: float,
                       current_value: float, monthly_sip: float = 0):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    INSERT INTO portfolio
    (session_id, asset_type, asset_name, invested, current_value, monthly_sip, start_date)
    VALUES (?,?,?,?,?,?,?)
    """, (session_id, asset_type, asset_name, invested,
          current_value, monthly_sip, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_portfolio(session_id: str) -> list:
    conn = get_connection()
    c    = conn.cursor()
    c.execute("""
    SELECT * FROM portfolio WHERE session_id=? ORDER BY invested DESC
    """, (session_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_portfolio_summary(session_id: str) -> dict:
    items = get_portfolio(session_id)
    if not items:
        return {"total_invested": 0, "total_current": 0,
                "total_gain": 0, "gain_pct": 0, "items": []}

    total_invested = sum(i["invested"] for i in items)
    total_current  = sum(i["current_value"] for i in items)
    total_gain     = total_current - total_invested
    gain_pct       = round((total_gain / total_invested * 100), 2) \
                     if total_invested > 0 else 0

    return {
        "total_invested": total_invested,
        "total_current":  total_current,
        "total_gain":     total_gain,
        "gain_pct":       gain_pct,
        "items":          items
    }