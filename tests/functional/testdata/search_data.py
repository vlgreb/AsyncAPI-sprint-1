from http import HTTPStatus

from .person_data import BEN_HOUSER_INFO

FILMS_SEARCH_STATUS_AND_LENGTH_QUERIES = [
    (
        {'query': 'The Star',
         'page_number': 1,
         'page_size': 25},
        {'status': HTTPStatus.OK, 'length': 25}
    ),
    (
        {'query': 'war of stars',
         'page_number': 1,
         'page_size': 25},
        {'status': HTTPStatus.OK, 'length': 25}
    ),
    (
        {'query': 'star wors',
         'page_number': 1,
         'page_size': 25},
        {'status': HTTPStatus.OK, 'length': 25}
    ),
    (
        {'query': 'wor stor',
         'page_number': 1,
         'page_size': 25},
        {'status': HTTPStatus.OK, 'length': 25}
    ),
    (
        {'query': 'foooooo123',
         'page_number': 1,
         'page_size': 25},
        {'status': HTTPStatus.NOT_FOUND, 'length': 1}
    )
]

STAR_WARS_TRILOGY_SHORT_INFO = [{
    "id": "dc2dbf5d-de5d-4153-a049-51ba44f15e04",
    "title": "Empire of Dreams: The Story of the 'Star Wars' Trilogy",
    "imdb_rating": 8.3
}]

STAR_WARS_OBI_WAN_SHORT_INFO = [
    {
        "id": "d6a7409f-87cd-49d7-8803-951a7352c2ce",
        "title": "Star Wars: Obi-Wan",
        "imdb_rating": 6.2
    }
]

FILM_FULL_TEXT_SEARCH = [
    (
        {'query': "Empire of Dreams: The Story of the 'Star Wars' Trilogy",
         'page_number': 1,
         'page_size': 1},
        STAR_WARS_TRILOGY_SHORT_INFO
    ),
    (
        {'query': 'Empire of Dreams Star Wars',
         'page_number': 1,
         'page_size': 1},
        STAR_WARS_TRILOGY_SHORT_INFO
    ),
    (
        {'query': 'the stae wars trilogi empire dreams',
         'page_number': 1,
         'page_size': 1},
        STAR_WARS_TRILOGY_SHORT_INFO
    ),
    (
        {'query': 'star wars obi one',
         'page_number': 1,
         'page_size': 1},
        STAR_WARS_OBI_WAN_SHORT_INFO
    ),
    (
        {'query': 'Star Wars: Obi-Wan',
         'page_number': 1,
         'page_size': 1},
        STAR_WARS_OBI_WAN_SHORT_INFO
    )
]

PERSONS_FUZZY_SEARCH_RESULT = [BEN_HOUSER_INFO]

PERSONS_FUZZY_SEARCH_QUERIES = [
    (
        {'query': 'Ben Houser',
         'page_number': 1,
         'page_size': 1},
        PERSONS_FUZZY_SEARCH_RESULT
    ),
    (
        {'query': 'ban houser',
         'page_number': 1,
         'page_size': 1},
        PERSONS_FUZZY_SEARCH_RESULT
    ),
    (
        {'query': 'bam houser',
         'page_number': 1,
         'page_size': 1},
        PERSONS_FUZZY_SEARCH_RESULT
    ),
    (
        {'query': 'bem houser',
         'page_number': 1,
         'page_size': 1},
        PERSONS_FUZZY_SEARCH_RESULT
    ),
    (
        {'query': 'ben houzer',
         'page_number': 1,
         'page_size': 1},
        PERSONS_FUZZY_SEARCH_RESULT
    )
]
