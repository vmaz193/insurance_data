-- This model aggregates trip data to the policy level.
-- It calculates total trips, distance, and driving events for each policy.

select
    policy_id,
    count(trip_id) as total_trips,
    sum(distance_miles) as total_distance_miles,
    avg(distance_miles) as average_distance_per_trip,
    sum(hard_braking_events) as total_hard_braking_events,
    sum(rapid_acceleration_events) as total_rapid_acceleration_events

from {{ ref('stg_telematics') }}

group by
    policy_id