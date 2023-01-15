WITH modified_genres AS (
    SELECT
        DISTINCT(gfw.film_work_id)
    FROM
        content.genre_film_work gfw
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE g.modified > {last_md_date}
), modified_persons AS (
    SELECT
        DISTINCT(pfw.film_work_id),
    FROM
        content.person_film_work pfw
        LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE p.modified > {last_md_date}
)
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created,
   fw.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE
    fw.modified > {last_md_date}
    OR fw.id IN modified_genres
    OR fw.id IN modified_persons
GROUP BY fw.id
ORDER BY fw.modified
LIMIT {batch_size};


-- SELECT
--    fw.id,
--    fw.title,
--    fw.description,
--    fw.rating,
--    fw.type,
--    fw.created,
--    fw.modified,
--    COALESCE (
--        json_agg(
--            DISTINCT jsonb_build_object(
--                'person_role', pfw.role,
--                'person_id', p.id,
--                'person_name', p.full_name
--            )
--        ) FILTER (WHERE p.id is not null),
--        '[]'
--    ) as persons,
--    array_agg(DISTINCT g.name) as genres
-- FROM content.film_work fw
-- LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
-- LEFT JOIN content.person p ON p.id = pfw.person_id
-- LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
-- LEFT JOIN content.genre g ON g.id = gfw.genre_id
-- WHERE fw.modified > '<время>'
-- GROUP BY fw.id
-- ORDER BY fw.modified
-- LIMIT 100;

-- SELECT
--    DISTINCT(gfw.film_work_id),
-- FROM
--     content.genre_film_work gfw
--     LEFT JOIN content.genre g ON g.id = gfw.genre_id
-- WHERE g.modified > '<время>'
-- ORDER BY gfw.film_work_id
-- LIMIT 100;


-- SELECT
--    DISTINCT(pfw.film_work_id),
-- FROM
--     content.person_film_work pfw
--     LEFT JOIN content.person p ON p.id = pfw.person_id
-- WHERE p.modified > '<время>'
-- ORDER BY pfw.film_work_id
-- LIMIT 100;

SELECT
   fw.id,
   fw.rating AS imdb_rating,
   array_agg(DISTINCT g.name) as genres,
   fw.title,
   fw.description,
   fw.modified,
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
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > '2021-05-04'
GROUP BY fw.id
ORDER BY fw.modified
LIMIT 2;

SELECT
   DISTINCT(gfw.film_work_id)
FROM
    content.genre_film_work gfw
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE g.modified > '<время>'
ORDER BY gfw.film_work_id
LIMIT 100;