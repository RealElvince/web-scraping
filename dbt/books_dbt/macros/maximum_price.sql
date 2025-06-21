{% macro calculate_maximum_price(source_model)%}
   SELECT 
      MAX(price) AS maximum_price
      FROM {{ ref(source_model)}}
{% endmacro %}