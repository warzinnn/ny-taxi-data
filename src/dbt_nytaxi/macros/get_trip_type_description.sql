{# This macro returns the description of the trip_type #}

{% macro get_trip_type_description(trip_type) %}

    CASE {{ trip_type }}
        WHEN 0 THEN 'Invalid'
        WHEN 1 THEN 'Street-hail'
        WHEN 2 THEN 'Dispatch'
    end

{% endmacro %}