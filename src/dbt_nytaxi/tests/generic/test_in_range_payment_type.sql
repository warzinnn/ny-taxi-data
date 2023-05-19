{% test test_in_range_payment_type(model, column_name) %}
-- Test that check is the values of a column is in the specified range

WITH validation AS (
    SELECT
        {{ column_name }} AS field_to_test
    FROM {{ model }}
),

validation_errors AS (
    SELECT
        field_to_test
    FROM validation
    WHERE field_to_test > 99
)

SELECT *
FROM validation_errors

{% endtest %}