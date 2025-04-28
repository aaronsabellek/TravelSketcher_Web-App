import requests

from flask import Blueprint, request, jsonify, current_app

search_bp = Blueprint('search', __name__)


@search_bp.route('/search-images', methods=['GET'])
def search_images():
    """Searches for images in Unsplash"""

    search_term = request.args.get('query')  # Get the search term from the query
    page = request.args.get('page', default=1, type=int)

    if not search_term:
        return jsonify({'error': 'No search term specified'}), 400

    # Unsplash API URL
    url = f"https://api.unsplash.com/search/photos?query={search_term}&page={page}&per_page=15"

    # Unsplash access key
    access_key = current_app.config['UNSPLASH_ACCESS_KEY']

    # Unsplash request with access Key
    response = requests.get(url, headers={'Authorization': f'Client-ID {access_key}'})

    if response.status_code != 200:
        return jsonify({'error': 'Fehler bei der Anfrage an Unsplash'}), 500

    # Extract relevant data
    data = response.json()

    results = []
    for image in data.get('results', []):
        urls = image.get('urls')
        if not urls or 'small' not in urls:
            continue

        results.append({
            'id': image.get('id', ''),
            'url': urls['small'],
            'alt_description': image.get('alt_description', 'No image description available')
        })

    return jsonify({'results': results})

