WITH source AS (

    SELECT * FROM {{ source('gabriel', 'capacity_parameters') }}

)

SELECT * FROM source