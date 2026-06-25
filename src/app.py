from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def search_torrent(query, result_limit=15):
    base_url = "https://torrentz2.nz/"
    search_url = base_url + "search?q=" + query

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result_divs = soup.find_all('div', class_='results')

        if result_divs:
            result_count = 0
            torrent_results = []

            for div in result_divs:
                for i, a in enumerate(div.find_all('a', href=True)):
                    if a.text:
                        result_count += 1

                        torrent_results.append({
                            'title': a.text,
                            'link': a['href']
                        })

                        if result_count >= result_limit:
                            break

                if result_count >= result_limit:
                    break

            return torrent_results

    else:
        return {"error": f"Error {response.status_code}: Unable to fetch the page."}

@app.route('/torrent_search', methods=['POST'])
def torrent_search():
    search_query = request.form['searchTerm']
    torrent_results = search_torrent(search_query)
    return jsonify(torrent_results)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['searchTerm']

        # Google search (replace with your actual Google search logic)
        google_results = []

        # Torrent search (using AJAX request)
        torrent_results = requests.post('http://127.0.0.1:5000/torrent_search', data={'searchTerm': search_query}).json()

        return render_template('index.html', google_results=google_results, torrent_results=torrent_results)

    return render_template('index.html', google_results=None, torrent_results=None)

