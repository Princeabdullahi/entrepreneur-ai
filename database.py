import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('business_data.db')
    c = conn.cursor()
    
    # Business Profile Table
    c.execute('''CREATE TABLE IF NOT EXISTS businesses
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  location TEXT,
                  product TEXT,
                  target_audience TEXT)''')
                  
    # Sales Data Table
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (date DATE,
                  business_id INTEGER,
                  revenue REAL,
                  expenses REAL,
                  PRIMARY KEY (date, business_id))''')

    # New table for streaks
    c.execute('''CREATE TABLE IF NOT EXISTS streaks
             (user_id INTEGER PRIMARY KEY,
              last_active DATE,
              streak_days INTEGER)''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
