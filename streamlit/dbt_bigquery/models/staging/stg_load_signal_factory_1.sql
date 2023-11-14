WITH source AS (

    SELECT * FROM {{ source('gabriel', 'load_signal_factory_1') }}

)

SELECT * FROM source