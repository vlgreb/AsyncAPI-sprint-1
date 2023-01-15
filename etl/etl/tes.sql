SELECT
    id as filmwork_id,
    filmwork.modified as updated_at
FROM content.film_work filmwork
WHERE
    filmwork.modified > '2021-05-20'
UNION
SELECT
    filmwork.id as filmwork_id,
    genre.modified as updated_at
FROM content.genre genre
    INNER JOIN content.genre_film_work genre_filmwork
        ON genre.id = genre_filmwork.genre_id
    INNER JOIN content.film_work filmwork
        ON genre_filmwork.film_work_id = filmwork.id
WHERE
    genre.modified > '2021-05-20'
UNION
SELECT
    filmwork.id as filmwrok_id,
    person.modified as updated_at
FROM content.person person
    INNER JOIN content.person_film_work person_filmwork
        ON person.id = person_filmwork.person_id
    INNER JOIN content.film_work filmwork
        ON person_filmwork.film_work_id = filmwork.id
WHERE
    person.modified > '2021-05-20'
ORDER BY
    updated_at
LIMIT 5;



--------------


SELECT
    gfw.film_work_id, fmw.title, g.modified as genre_modified, fmw.modified as film_modified
FROM
    content.genre_film_work gfw
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    LEFT JOIN content.film_work fmw ON gfw.film_work_id = fmw.id
WHERE g.modified > '1970-05-01'
ORDER BY g.modified, fmw.modified
LIMIT 100;


--WITH modified_genres AS (
--    SELECT
--        DISTINCT(gfw.film_work_id), g.modified
--    FROM
--        content.genre_film_work gfw
--        LEFT JOIN content.genre g ON g.id = gfw.genre_id
--    WHERE g.modified > '1970-05-01'
--    ORDER BY g.modified
--    LIMIT 100
--), modified_persons AS (
--    SELECT
--        DISTINCT(pfw.film_work_id), p.modified
--    FROM
--        content.person_film_work pfw
--        LEFT JOIN content.person p ON p.id = pfw.person_id
--    WHERE p.modified > '1970-05-01'
--    ORDER BY p.modified
--    LIMIT 100
--)
--SELECT
--    gfw.film_work_id, fmw.title, g.modified as genre_modified, fmw.modified as film_modified
--FROM
--    content.genre_film_work gfw
--    LEFT JOIN content.genre g ON g.id = gfw.genre_id
--    LEFT JOIN content.film_work fmw ON gfw.film_work_id = fmw.id
--WHERE g.modified > '1970-05-01'
--ORDER BY g.modified, fmw.modified
--LIMIT 100;

--WITH modified_genres AS (
--    SELECT
--        DISTINCT(gfw.film_work_id), g.modified
--    FROM
--        content.genre_film_work gfw
--        LEFT JOIN content.genre g ON g.id = gfw.genre_id
--    WHERE g.modified > '1970-05-01'
--    ORDER BY g.modified
--    LIMIT 100
--), modified_persons AS (
--    SELECT
--        DISTINCT(pfw.film_work_id), p.modified
--    FROM
--        content.person_film_work pfw
--        LEFT JOIN content.person p ON p.id = pfw.person_id
--    WHERE p.modified > '1970-05-01'
--    ORDER BY p.modified
--    LIMIT 100
--), md_g_p AS (
--    SELECT film_work_id, modified FROM modified_genres
--    UNION modified_persons
--)
--SELECT
--    fmw.film_work_id,
--    fmw.title,
--    fmw.modified as modified
--FROM
--    content.film_work fmw
--    LEFT JOIN modified_genres mdg ON mdg.film_work_id = fmw.id
--    LEFT JOIN modified_persons mdp ON mdp.film_work_id = fmw.id
--WHERE fmw.modified > '1970-05-01'
--GROUP BY
--    fmw.title, film_modified, genre_modified, person_modified
--ORDER BY film_modified, genre_modified, person_modified
--LIMIT 100;


--WITH modified_genres AS (
--    SELECT
--        DISTINCT(gfw.film_work_id), g.modified
--    FROM
--        content.genre_film_work gfw
--        LEFT JOIN content.genre g ON g.id = gfw.genre_id
--    WHERE g.modified > '1970-05-01'
--    ORDER BY g.modified
--    LIMIT 100
--), modified_persons AS (
--    SELECT
--        DISTINCT(pfw.film_work_id), p.modified
--    FROM
--        content.person_film_work pfw
--        LEFT JOIN content.person p ON p.id = pfw.person_id
--    WHERE p.modified > '1970-05-01'
--    ORDER BY p.modified
--    LIMIT 100
--), md_g_p AS (
--    SELECT film_work_id, modified FROM modified_genres
--    UNION
--    SELECT film_work_id, modified FROM modified_persons
--    GROUP BY film_work_id, modified
--    ORDER BY modified
--)
--SELECT
--    title,
--    film_work_id,
--    fmw.modified as film_work_modified,
--    md_g_p.modified as g_p_modified
--FROM md_g_p
--    LEFT JOIN content.film_work fmw ON fmw.id = film_work_id
--LIMIT 100;

WITH modified_genres AS (
    SELECT
        gfw.film_work_id, g.modified
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > '1970-05-01'
), modified_persons AS (
    SELECT
        pfw.film_work_id, p.modified
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > '1970-05-01'
), modified_filmworks AS (
    SELECT
        id, modified
    FROM
        content.film_work
    WHERE modified > '1970-05-01'
),
md_g_p AS (
    SELECT film_work_id, modified FROM modified_genres
    UNION
    SELECT * FROM modified_persons
    UNION
    SELECT * FROM modified_filmworks
    GROUP BY film_work_id, modified
    ORDER BY modified
    LIMIT 100
)
SELECT
    title,
    film_work_id,
    fmw.modified as film_work_modified,
    md_g_p.modified as g_p_modified
FROM md_g_p
    LEFT JOIN content.film_work fmw ON fmw.id = film_work_id
LIMIT 100;


--WITH modified_genres AS (
--    SELECT
--        gfw.film_work_id, g.modified
--    FROM
--        content.genre_film_work gfw
--        LEFT JOIN content.genre g ON g.id = gfw.genre_id
--    WHERE g.modified > '1970-05-01'
--), modified_persons AS (
--    SELECT
--        pfw.film_work_id, p.modified
--    FROM
--        content.person_film_work pfw
--        LEFT JOIN content.person p ON p.id = pfw.person_id
--    WHERE p.modified > '1970-05-01'
--)
--md_g_p AS (
--    SELECT film_work_id, modified FROM modified_genres
--    UNION
--    SELECT film_work_id, modified FROM modified_persons
--    GROUP BY film_work_id, modified
--    ORDER BY modified
--)
--SELECT
--    title,
--    film_work_id,
--    fmw.modified as film_work_modified,
--    md_g_p.modified as g_p_modified
--FROM md_g_p
--    LEFT JOIN content.film_work fmw ON fmw.id = film_work_id
--LIMIT 100;

WITH modified_genres AS (
    SELECT
        gfw.film_work_id, g.modified
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > '1970-05-01'
), modified_persons AS (
    SELECT
        pfw.film_work_id, p.modified
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > '1970-05-01'
), modified_filmworks AS (
    SELECT
        id as film_work_id, modified
    FROM
        content.film_work
    WHERE modified > '1970-05-01'
)
SELECT film_work_id, modified FROM modified_genres
UNION
SELECT * FROM modified_persons
UNION
SELECT * FROM modified_filmworks
GROUP BY film_work_id, modified
ORDER BY modified
LIMIT 100;


-----------

WITH modified_genres AS (
    SELECT
        gfw.film_work_id, g.modified
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > '{last_md_date}'
), modified_persons AS (
    SELECT
        pfw.film_work_id, p.modified
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > '{last_md_date}'
), modified_filmworks AS (
    SELECT
        id as film_work_id, modified
    FROM
        content.film_work
    WHERE modified > '{last_md_date}'
), ordered_records AS (
    SELECT film_work_id, modified FROM modified_genres
    UNION
    SELECT * FROM modified_persons
    UNION
    SELECT * FROM modified_filmworks
)
SELECT
   fw.id,
   fw.rating AS imdb_rating,
   array_agg(DISTINCT g.name) as genres,
   fw.title,
   fw.description,
   ordered_records.modified,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'writer'),
       '[]'
   ) as writers
FROM ordered_records
LEFT JOIN content.film_work fw ON ordered_records.film_work_id = fw.id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
GROUP BY fw.id, ordered_records.modified
ORDER BY ordered_records.modified
LIMIT {batch_size};

--SELECT
--   DISTINCT(gfw.film_work_id)
--FROM
--    content.genre_film_work gfw
--    LEFT JOIN content.genre g ON g.id = gfw.genre_id
--WHERE g.modified > '<время>'
--ORDER BY gfw.film_work_id
--LIMIT 100;


----------

WITH modified_genres AS (
    SELECT
        gfw.film_work_id, g.modified
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > '1970-05-01'
), modified_persons AS (
    SELECT
        pfw.film_work_id, p.modified
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > '1970-05-01'
), modified_filmworks AS (
    SELECT
        id as film_work_id, modified
    FROM
        content.film_work
    WHERE modified > '1970-05-01'
), ordered_records AS (
    SELECT film_work_id, modified FROM modified_genres
    UNION
    SELECT * FROM modified_persons
    UNION
    SELECT * FROM modified_filmworks
)
SELECT
   fw.id,
   fw.rating AS imdb_rating,
   array_agg(DISTINCT g.name) as genres,
   fw.title,
   fw.description,
--   ordered_records.modified,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
   array_agg(p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'writer'),
       '[]'
   ) as writers
FROM ordered_records
LEFT JOIN content.film_work fw ON ordered_records.film_work_id = fw.id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
GROUP BY fw.id, ordered_records.modified
ORDER BY ordered_records.modified
LIMIT 100;





WITH modified_genres AS (
    SELECT
        gfw.film_work_id, g.modified
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > '1970-05-01'
), modified_persons AS (
    SELECT
        pfw.film_work_id, p.modified
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > '1970-05-01'
), modified_filmworks AS (
    SELECT
        id as film_work_id, modified
    FROM
        content.film_work
    WHERE modified > '1970-05-01'
), ordered_records AS (
    SELECT film_work_id, modified FROM modified_genres
    UNION
    SELECT * FROM modified_persons
    UNION
    SELECT * FROM modified_filmworks
)
SELECT
   fw.id,
   coalesce(array_agg(p.full_name) FILTER (WHERE pfw.role = 'director'), '{}') AS director
FROM ordered_records
LEFT JOIN content.film_work fw ON ordered_records.film_work_id = fw.id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
GROUP BY fw.id
HAVING fw.id = '479f20b0-58d1-4f16-8944-9b82f5b1f22a';