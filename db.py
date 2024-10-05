import sqlite3

# SQLiteデータベースに接続（データベースが存在しない場合は新しく作成）
conn = sqlite3.connect('projects.db')

# カーソルを作成
cursor = conn.cursor()

# テーブル作成のSQL文
create_table_sql = '''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    language TEXT,
    framework TEXT
    
);
'''


# テーブルを作成
cursor.execute(create_table_sql)
conn.commit()

def get_db_connection():
    conn = sqlite3.connect('projects.db')
    return conn


# 記事を挿入する例
def insert_project(title, description, url, language, framework):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_sql = '''
    INSERT INTO projects (title, description, url, language, framework)
    VALUES (?, ?, ?, ?, ?);
    '''
    
    cursor.execute(insert_sql, (title, description, url, language, framework))
    conn.commit()
    conn.close()
