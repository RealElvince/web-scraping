SELECT DISTINCT rating
FROM {{ ref('stg_books') }}
