from http import HTTPStatus

BEN_HOUSER_INFO = {
  "id": "54f86b6e-510a-4507-90d4-527cad27a644",
  "full_name": "Ben Houser",
  "role": [
    "writer"
  ],
  "film_ids": [
    "943946ed-4a2b-4c71-8e0b-a58a11bd1323"
  ]
}

PETRI_LEHTINEN_FILMS = {
  "id": "f0a2f64b-3531-4b1f-92c7-cca01769fe1c",
  "films": [
    {
      "id": "28b7b1ac-8834-45b7-a02e-528d48fe476c",
      "title": "Star Wreck IV: The Kilpailu",
      "imdb_rating": 6
    },
    {
      "id": "2bb5d323-0e56-4f86-ae38-34c63fffb7bf",
      "title": "Star Wreck 3",
      "imdb_rating": 6
    }
  ]
}

FILMS_WITH_PERSON_PARAMS = [
  (
    f"/{PETRI_LEHTINEN_FILMS['id']}/film",
    PETRI_LEHTINEN_FILMS['films']
  ),
  (
    "/NoneBadPerson",
    {"detail": "person not found"}
  ),
]

PERSONS_PAGINATION_PARAMS = [
  (
    {'page_number': 1,
     'page_size': 25},
    {'status': HTTPStatus.OK, 'length': 25}
  ),
  (
    {'page_number': 1,
     'page_size': 50},
    {'status': HTTPStatus.OK, 'length': 50}
  ),
  (
    {'page_number': 1,
     'page_size': 100},
    {'status': HTTPStatus.OK, 'length': 100}
  ),
  (
    {'page_number': -1,
     'page_size': 50},
    {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
  ),

  (
    {'page_number': 'one',
     'page_size': 50},
    {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
  ),
  (
    {'page_number': 1,
     'page_size': 'fifty'},
    {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
  )
]

PERSONS_LIST_REQUEST_STATUS = [
  (
    '',
    {'status': HTTPStatus.OK, 'length': 25}
  ),
  (
    '/e6e2026b-961b-4d93-aa96-1083e77e179d',
    {'status': HTTPStatus.OK, 'length': 4}
  ),
  (
    '/54f86b6e-510a-4507-90d4-nosuchdataaa',
    {'status': HTTPStatus.NOT_FOUND, 'length': 1}
  )
]

PERSON_BY_ID_PARAMS = [
  (
    '/54f86b6e-510a-4507-90d4-527cad27a644',
    BEN_HOUSER_INFO
  ),
  (
    "/NoneBadPerson",
    {"detail": "person not found"}
  )
]


TEST_PERSON_CACHE = [
  (
    '/54f86b6e-510a-4507-90d4-527cad27a644',
    BEN_HOUSER_INFO
  )
]


LAST_PAGE_PERSONS = [
  {
      "id": "1c9e15e5-cce8-4c57-9366-57c748583d33",
      "full_name": "Achim Podak"
  },
  {
      "id": "6c1dbabf-ce35-4471-b222-67e1ac052956",
      "full_name": "Acey Aguilar"
  },
  {
      "id": "ed63a508-4f7c-4dc6-84c3-482f4d08a582",
      "full_name": "Abraham Benrubi"
  },
  {
      "id": "5deae4c9-388f-4468-983c-28b4075bd6f0",
      "full_name": "Abir Chatterjee"
  },
  {
      "id": "533c5cdd-a9ef-4345-a9b5-02b6382d78c8",
      "full_name": "Abigail Lawrie"
  },
  {
      "id": "8b58b717-e469-4f61-92bc-8fe6302e7abd",
      "full_name": "Abe Kwong"
  },
  {
      "id": "9e8559d3-5529-4313-9ea1-cb0c8b46f232",
      "full_name": "Abbie Cornish"
  },
  {
      "id": "2570419f-0ec7-4aac-8af6-f322e41e02fb",
      "full_name": "Aaron de Orive"
  },
  {
      "id": "f00ac91a-b19a-4511-b510-fd05a4a52cbb",
      "full_name": "Aaron Malchow"
  },
  {
      "id": "4959e5b7-d157-4cdf-bc4f-5eb3cf8bd57f",
      "full_name": "Aaron Ginn-Forsberg"
  },
  {
      "id": "cbdb2ba5-39c9-4093-b2bd-95f4e62bdb6d",
      "full_name": "Aaron Contreras"
  },
  {
      "id": "4b3662a9-bb59-46bb-b422-fda62c9891b5",
      "full_name": "Aaron Barzman"
  },
  {
      "id": "e6a1d07f-8fdc-4323-803f-9c34edb718bd",
      "full_name": "Aarno Sulkanen"
  },
  {
      "id": "afa97a6e-9dbf-4468-8f1f-542ff8231e87",
      "full_name": "A.F. Erickson"
  },
  {
      "id": "8fb635c2-913f-4e70-bfec-404a5c7f7646",
      "full_name": "A. Edward Sutherland"
  },
  {
      "id": "2871f883-e001-4848-92d0-002adbdf2547",
      "full_name": "'Tobba' Thorbjorg Valdis Kristjansdottir"
  }
]
