import uuid
from typing import List


def get_movies_list(size) -> List[dict]:
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genres': [
            {'id': 'genre1', 'name': 'Action'},
            {'id': 'genre2', 'name': 'Sci-Fi'}
        ],
        'creation_date': 2022,
        'title': 'The Star',
        'description': 'New World',
        'actors': [
            {'id': '111', 'full_name': 'Ann'},
            {'id': '222', 'full_name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'full_name': 'Ben'},
            {'id': '444', 'full_name': 'Howard'}
        ],
        'directors': [
            {'id': '555', 'full_name': 'Igor'},
            {'id': '777', 'full_name': 'Vladimir'}
        ]
    } for _ in range(size)]

    return [
        {
            '_index': 'movies',
            '_id': row['id'],
            '_source': row
        } for row in es_data
    ]
