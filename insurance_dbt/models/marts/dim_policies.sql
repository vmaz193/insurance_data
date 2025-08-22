-- This model provides a detailed view of each policy, enriched with
-- aggregated driving data from the telematics summary.

with policies as (
    select * from {{ ref('stg_policies') }}
),

telematics_summary as (
    select * from {{ ref('int_telematics_summary') }}
)

select
    -- Policy Identifiers
    p.policy_id,

    -- Policy Attributes
    p.policy_start_date,
    p.policy_end_date,
    p.annual_premium,
    p.vehicle_year,
    p.has_telematics_subscription,

    -- Aggregated Telematics Data
    coalesce(t.total_trips, 0) as total_trips,
    coalesce(t.total_distance_miles, 0) as total_distance_miles,
    coalesce(t.total_hard_braking_events, 0) as total_hard_braking_events,
    coalesce(t.total_rapid_acceleration_events, 0) as total_rapid_acceleration_events

from policies p

left join telematics_summary t
    on p.policy_id = t.policy_id