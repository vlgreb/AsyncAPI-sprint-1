PERSONS_SETTINGS = {
    "type": "nested",
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "full_name": {
            "type": "text",
            "analyzer": "ru_en"
        }
    }
}

GENRE_SETTINGS = {
    "id": {
        "type": "keyword"
    },
    "name": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
            "raw": {
                "type": "keyword"
            }
        }
    }
}

TEXT_SETTINGS = {
    "type": "text",
    "analyzer": "ru_en"
}

TEXT_KEYWORD_SETTINGS = {
    "type": "text",
    "analyzer": "ru_en",
    "fields": {
        "raw": {
            "type": "keyword"
        }
    }
}

movies_index = {
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "float"
            },
            "genres": {
                "type": "nested",
                "dynamic": "strict",
                "properties": GENRE_SETTINGS
            },
            "creation_date": {
                "type": "date"
            },
            "title": TEXT_KEYWORD_SETTINGS,
            "description": TEXT_SETTINGS,
            "actors": PERSONS_SETTINGS,
            "writers": PERSONS_SETTINGS,
            "directors": PERSONS_SETTINGS
        }
    }
}

genre_index = {
    "mappings": {
        "dynamic": "strict",
        "properties": GENRE_SETTINGS
    }
}

person_index = {
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "full_name": TEXT_KEYWORD_SETTINGS,
            "role": TEXT_KEYWORD_SETTINGS,
            "film_ids": {
                "type": "keyword"
            }
        }
    }
}
