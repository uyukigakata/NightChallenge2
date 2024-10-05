import sqlite3
import requests
from bs4 import BeautifulSoup
import os

YEAR = 2019  # 本来は2017から

class Scraping:
    def __init__(self, start_year=YEAR):
        self.start_year = start_year
        self.db_file = 'projects.db'
        self.create_table()

    def get_db_connection(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        # 既存のデータベースファイルを削除
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT,
            year INTEGER,
            language TEXT,
            framework TEXT
        );
        '''
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()

    def insert_project(self, title, description, url, year, language=None, framework=None):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        insert_sql = '''
        INSERT INTO projects (title, description, url, year, language, framework)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        cursor.execute(insert_sql, (title, description, url, year, language, framework))
        conn.commit()
        conn.close()

    def scrape_projects(self):
        year = self.start_year
        while True:
            url = f"https://sechack365.nict.go.jp/achievement/{year}/"
            response = requests.get(url)
            if response.status_code != 200:
                break
            
            self.parse_and_store_projects(response, url, year)
            year += 1

    def parse_and_store_projects(self, response, url, year):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if year >= 2022:
            titles = soup.find_all(class_='title')[1:]  # 最初の要素をスキップ
            texts = soup.find_all(class_='text')
        else:
            titles = soup.find_all(class_='a_ttl')
            texts = soup.find_all(class_='a_txt')
        
        for title, text in zip(titles, texts):
            if year >= 2022 and (title.find_parent(class_='scroll_table') or text.find_parent(class_='scroll_table')):
                continue
            
            title_text = title.get_text(strip=True)
            text_content = text.get_text(strip=True)
            
            self.insert_project(title_text, text_content, url, year)

# 使用方法
scraper = Scraping()
scraper.scrape_projects()
#終了