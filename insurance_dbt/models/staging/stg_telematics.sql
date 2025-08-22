select
    -- IDs
    trip_id,
    policy_id,
    
    -- Trip Details
    trip_date::date as trip_date,
    distance_miles,
    hard_braking_events,
    rapid_acceleration_events

from {{ source('raw', 'trips') }}