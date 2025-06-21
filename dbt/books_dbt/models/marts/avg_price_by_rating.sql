WITH cte_avg_price_by_rating AS (
    SELECT
        rating,
        ROUND(AVG(price), 2) AS avg_price
    FROM {{ ref('stg_books') }}
    GROUP BY rating
)

SELECT * FROM cte_avg_price_by_rating