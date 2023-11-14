WITH source AS (

    SELECT * FROM {{ source('gabriel', 'load_signal_factory_2') }}

)

SELECT * FROM source