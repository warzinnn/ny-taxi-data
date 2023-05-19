{# This macro returns the description of the RatecodeID #}

{% macro get_rate_code_description(RatecodeID) %}

    CASE {{ RatecodeID }}
        WHEN 1 THEN 'Standard rate'
        WHEN 2 THEN 'JFK'
        WHEN 3 THEN 'Newark'
        WHEN 4 THEN 'Nassau or Westchester'
        WHEN 5 THEN 'Negotiated fare'
        WHEN 6 THEN 'Group ride'
        ELSE 'Invalid'
    end

{% endmacro %}