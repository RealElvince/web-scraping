WITH stg_books AS(
    SELECT
        book_title,
        price,
        rating
    FROM {{ source('online_books', 'books') }}
)

SELECT * FROM stg_books