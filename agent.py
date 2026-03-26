import requests
from bs4 import BeautifulSoup
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import webbrowser

def display_html(topic, data, summary):
    html_content = f"""
    <html>
    <head>
        <title>AI Agent Result</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #16a085; }}
            p {{ line-height: 1.6; }}
            .box {{ background: #f4f4f4; padding: 15px; margin-bottom: 20px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <h1>🤖 AI Research Agent</h1>
        <h2>Topic: {topic}</h2>

        <div class="box">
            <h3>🔎 Fetched Data</h3>
            {''.join(f"<p>{d}</p>" for d in data)}
        </div>

        <div class="box">
            <h3>🧠 Summary</h3>
            <p>{summary}</p>
        </div>
    </body>
    </html>
    """

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html_content)

webbrowser.open("file://" + os.path.realpath("output.html"))
# Initialize OpenAI client


def fetch_data(query):
    headers = {"User-Agent": "Mozilla/5.0"}

    variations = [
        query,
        query + " machine learning",
        query + " artificial intelligence"
    ]

    for q in variations:
        search_url = f"https://en.wikipedia.org/w/index.php?search={q.replace(' ', '+')}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.select(".mw-search-result-heading a")

        if results:
            link = "https://en.wikipedia.org" + results[0]["href"]

            page = requests.get(link, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")

            paragraphs = soup.find_all("p")

            data = []
            for p in paragraphs:
                text = p.get_text().strip()

                if (
                    len(text) > 100
                    and "may refer to" not in text.lower()
                    and "does not exist" not in text.lower()
                ):
                    data.append(text)

            if data:
                return data[:5], link   # ✅ return link also

    return ["No meaningful data found."], None

def summarize(data):
    if not data or "No meaningful" in data[0]:
        return "No data available."
    
    # combine all text into one answer
    combined = " ".join(data)
    
    # simple clean explanation
    return combined[:600] + "..."

if __name__ == "__main__":
    print("🤖 AI Research Agent Started (type 'exit' to quit)\n")

    while True:
        query = input("Enter topic: ")

        if query.lower() == "exit":
            print("👋 Exiting agent...")
            break

        data = fetch_data(query)
        summary = summarize(data)
        display_html(query, data, summary)
        print("\n" + "="*60 + "\n")