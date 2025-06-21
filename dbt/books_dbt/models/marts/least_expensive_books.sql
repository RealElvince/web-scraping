WITH cte_least_expensive_books AS (
    SELECT *
    FROM {{ ref('stg_books') }}
    ORDER BY price ASC
    LIMIT 5
)

SELECT * FROM cte_least_expensive_books
