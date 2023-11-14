{{ config(materialized='table') }}

WITH capacity AS (
SELECT
  Day_of_the_Week AS day,
  line,
  capacity,
  Sc AS scenario
FROM
  {{ ref('stg_capacity_parameters')}}
UNPIVOT (capacity FOR line IN (Line_1, Line_2, Line_3, Line_4, Line_5))
),

load_factory_1 AS (
    SELECT
      *
    FROM
    {{ ref('stg_load_signal_factory_1')}}
),

load_factory_2 AS (
    SELECT
      *
    FROM
    {{ ref('stg_load_signal_factory_2')}}
)

SELECT
  capacity.day,
  capacity.line,
  capacity.capacity,
  scenario,
  SUM(COALESCE(load_factory_1.load, 0) + COALESCE(load_factory_2.load, 0)) AS load_all_factories
FROM
  capacity
  LEFT JOIN
    load_factory_1
      ON capacity.day = load_factory_1.day
      AND capacity.line = REPLACE(load_factory_1.line, '-', ' ')
  LEFT JOIN
    load_factory_2
      ON capacity.day = load_factory_2.day
      AND capacity.line = REPLACE(load_factory_2.line, '-', ' ')
GROUP BY
  day,
  line,
  capacity,
  scenario