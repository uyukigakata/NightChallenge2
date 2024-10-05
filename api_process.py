import google.generativeai as genai
import time

key = "APIのキー"

genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-1.5-flash')

with open("titles.txt", "r") as f:
    titles = f.readlines()
with open("descriptions.txt", "r") as f:
    descriptions = f.readlines()

for title, description in zip(titles, descriptions):
    print("title: ", title)
    print("description: ", description)

    res = model.generate_content(f"""""")
    print(res)
    time.sleep(10)

