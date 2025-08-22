select
    -- IDs
    alert_id,
    customer_id,
    account_id,

    -- Dates
    signup_date::date as signup_date,
    alert_date::date as alert_date,
    
    -- Alert Details
    alert_type,
    alert_status

from {{ source('raw', 'identity_protection') }}