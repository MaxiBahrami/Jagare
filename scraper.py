import requests
from bs4 import BeautifulSoup

# Define URLs for news and activities
url = 'https://jagareforbundet.se/mitt/stockholms-lan/jagareforbundet-stockholm/'

# Send request and parse content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Placeholder lists for news and activities
news_list = []
activities_list = []

# Extract news
news_items = soup.find_all('div', class_='newsItem newsItemFull')
for item in news_items:
    title = item.find('h2').text.strip()
    link = item.find('h2').a['href']
    # Extract the news text
    news_text = item.find('p').text.strip() if item.find('p') else "No additional text available."
    news_list.append((title, link, news_text))

# Extract activities
activities = soup.find('ul', id='listevents').find_all('li')
for activity in activities:
    date = f"{activity.find('div', class_='eventday').text.strip()} {activity.find('div', class_='eventmonth').text.strip()}"
    title = activity.find('a').text.strip()
    activities_list.append((date, title))

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
            <ul>{"".join(f"<li><a href='{link}'>{title}</a><p>{text}</p></li>" for title, link, text in news_list)}</ul>
        </div>
        <div class="activities">
            <h2>Activities</h2>
            <ul>{"".join(f"<li>{date}: {title}</li>" for date, title in activities_list)}</ul>
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
