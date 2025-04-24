from flask import Flask, render_template, request, jsonify
from ai_analyzer import BusinessAnalyzer
import sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
analyzer = BusinessAnalyzer()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/streak', methods=['POST'])
def update_streak():
    user_id = request.form['user_id']
    today = datetime.now().date()
    
    with sqlite3.connect('business_data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT last_active, streak_days FROM streaks WHERE user_id=?', (user_id,))
        row = c.fetchone()
        
        if row:
            last_active, streak = row
            last_active = datetime.strptime(last_active, "%Y-%m-%d").date()
            streak = streak + 1 if (today - last_active).days == 1 else 1
        else:
            streak = 1
            
        c.execute('''REPLACE INTO streaks VALUES (?,?,?)''',
                 (user_id, today, streak))
    
    return jsonify({'streak': streak})
    
@app.route('/analyze', methods=['POST'])
def analyze_business():
    # Get form data
    business_data = {
        'name': request.form['name'],
        'location': request.form['location'],
        'product': request.form['product'],
        'target': request.form['target']
    }
    
    # Get sales data
    sales = []
    for entry in request.form.getlist('sales[]'):
        date, revenue, expenses = entry.split('|')
        sales.append({
            'date': datetime.strptime(date, "%Y-%m-%d"),
            'revenue': float(revenue),
            'expenses': float(expenses)
        })
    
    # Save to DB (simplified)
    with sqlite3.connect('business_data.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO businesses VALUES (NULL,?,?,?,?)', 
                 (business_data['name'], business_data['location'], 
                  business_data['product'], business_data['target']))
        business_id = c.lastrowid
        
        for entry in sales:
            c.execute('INSERT INTO sales VALUES (?,?,?,?)',
                     (entry['date'], business_id, entry['revenue'], entry['expenses']))
    
    # Generate analysis
    sales_df = pd.DataFrame(sales)
    analysis = analyzer.generate_recommendations(business_data, sales_df)
    
    return jsonify({
        'business': business_data,
        'analysis': analysis
    })

if __name__ == '__main__':
    app.run(debug=True)
