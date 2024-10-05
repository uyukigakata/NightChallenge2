from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# データベース接続
def get_db_connection():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['search_input']
    conn = get_db_connection()
    
    query = '''
    SELECT DISTINCT *
    FROM projects 
    WHERE title LIKE ? 
    OR description LIKE ? 
    OR language LIKE ? 
    OR framework LIKE ?
    GROUP BY title
    ORDER BY year DESC, title
    '''

    search_param = f'%{keyword}%'
    results = conn.execute(query, (search_param, search_param, search_param, search_param)).fetchall()
    conn.close()
    
    if results:
        return render_template('result.html', results=results)
    else:
        return render_template('result.html', no_results=True)

if __name__ == '__main__':
    app.run(debug=True)