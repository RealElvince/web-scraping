{% macro calculate_minimum_price(source_model) %}
   SELECT
      MIN(price) AS minimum_price
   FROM {{ ref(source_model) }}
{% endmacro %}
