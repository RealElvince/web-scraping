WITH cte_most_expensive_books AS (

    SELECT *
FROM {{ ref('stg_books') }}
ORDER BY price DESC
LIMIT 5

)

SELECT * FROM cte_most_expensive_books
