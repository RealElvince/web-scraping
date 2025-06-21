SELECT 
    book_title,
    price,
    rating
FROM {{ ref('stg_books') }}
WHERE rating IS NOT NULL
AND price IS NOT NULL
AND book_title IS NOT NULL
AND book_title != ''