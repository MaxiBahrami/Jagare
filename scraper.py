import requests
from bs4 import BeautifulSoup
import sqlite3

# URL for scraping
url = 'https://jagareforbundet.se/mitt/stockholms-lan/jagareforbundet-stockholm/'

def scrape_and_update_db():
    # Send request and parse content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract news
    news_items = soup.find_all('div', class_='newsItem newsItemFull')
    news_list = [(item.find('h2').text.strip(), item.find('h2').a['href'], item.find('p').text.strip() if item.find('p') else "No additional text available.") for item in news_items]

    # Extract activities
    activities = soup.find('ul', id='listevents').find_all('li')
    activities_list = [(f"{activity.find('div', class_='eventday').text.strip()} {activity.find('div', class_='eventmonth').text.strip()}", activity.find('a').text.strip()) for activity in activities]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()

    # Create tables if they do not exist
    c.execute('''CREATE TABLE IF NOT EXISTS News (title TEXT, link TEXT, text TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Activities (date TEXT, title TEXT)''')

    # Insert news and activities into the database
    c.executemany("INSERT INTO News (title, link, text) VALUES (?, ?, ?)", news_list)
    c.executemany("INSERT INTO Activities (date, title) VALUES (?, ?)", activities_list)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def generate_html():
    # Connect to the database and fetch data
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM News")
    all_news = c.fetchall()
    c.execute("SELECT * FROM Activities")
    all_activities = c.fetchall()
    conn.close()

    # Generate HTML content
    html_content = f"""
    <html>
    <head>
        <title>Scraped Content</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
            .container {{ padding: 20px; }}
            .news, .activities {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .news {{ background-color: #f9f9f9; }}
            .activities {{ background-color: #e9ffe9; }}
            header, footer {{ background-color: #f0f0f0; padding: 10px; text-align: center; }}
        </style>
    </head>
    <body>
        <header>
            <h1>Scraped Content</h1>
        </header>
        <div class="container">
            <div class="news">
                <h2>News</h2>
                <ul>{"".join(f"<li><a href='{link}'>{title}</a><p>{text}</p></li>" for title, link, text in all_news)}</ul>
            </div>
            <div class="activities">
                <h2>Activities</h2>
                <ul>{"".join(f"<li>{date}: {title}</li>" for date, title in all_activities)}</ul>
            </div>
        </div>
        <footer>
            <p>Footer Content</p>
        </footer>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open("scraped_content.html", "w", encoding='utf-8') as file:
        file.write(html_content)

    print("HTML file has been successfully generated.")

def add_news_to_database(title, link, text):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO News (title, link, text) VALUES (?, ?, ?)", (title, link, text))
    conn.commit()
    conn.close()
    print("News item added successfully.")

if __name__ == "__main__":
    # 'scrape', 'add', or 'generate_html'
    action = input("Enter action (scrape, add, generate_html): ")
    
    if action == 'scrape':
        scrape_and_update_db()
    elif action == 'generate_html':
        generate_html()
    elif action == 'add':
        title = input("Enter news title: ")
        link = input("Enter news link: ")
        text = input("Enter news text: ")
        add_news_to_database(title, link, text)
