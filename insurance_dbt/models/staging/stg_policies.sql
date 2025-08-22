select
    -- IDs
    policy_id,
    customer_id,

    -- Customer Details
    state,
    zip_code,
    age as customer_age,
    
    -- Policy Details
    vehicle_year,
    policy_start_date::date as policy_start_date,
    policy_end_date::date as policy_end_date,
    monthly_premium_usd as monthly_premium,
    (monthly_premium_usd * 12) as annual_premium, -- Calculated field
    has_telematics_subscription

from {{ source('raw', 'policies') }}