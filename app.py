import requests
from bs4 import BeautifulSoup


import streamlit as st
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

st.title("🤖 AI Research Agent")

query = st.text_input("Ask anything:")

if query:
    data, link = fetch_data(query)
    answer = summarize(data)

    st.subheader("🧠 Answer")
    st.write(answer)

    if link:
        st.markdown(f"🔗 Source: [Read more]({link})")