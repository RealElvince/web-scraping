WITH cte_price_buckets AS (
   SELECT 
  book_title,
  price,
  rating,
  CASE
    WHEN price < 20 THEN 'Low'
    WHEN price BETWEEN 20 AND 40 THEN 'Medium'
    ELSE 'High'
  END AS price_bucket
FROM {{ ref('stg_books') }}
)


SELECT * FROM cte_price_buckets
