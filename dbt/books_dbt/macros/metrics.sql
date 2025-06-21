{% macro calculate_book_metrics(source_model) %}
    WITH numbered_ratings AS (
        SELECT
            price,
            CASE rating
                WHEN 'One' THEN 1
                WHEN 'Two' THEN 2
                WHEN 'Three' THEN 3
                WHEN 'Four' THEN 4
                WHEN 'Five' THEN 5
            END AS numeric_rating
        FROM {{ ref(source_model) }}
    )

    SELECT
        ROUND(SUM(price), 2) AS total_price,
        ROUND(AVG(price), 2) AS avg_price,
        ROUND(AVG(numeric_rating), 2) AS avg_rating
    FROM numbered_ratings
{% endmacro %}
