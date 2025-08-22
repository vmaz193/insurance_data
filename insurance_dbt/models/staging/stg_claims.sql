select
    -- IDs
    claim_id,
    policy_id,

    -- Dates
    incident_date::date as incident_date,
    claim_filed_date::date as claim_filed_date,

    -- Claim Details
    claim_type,
    claim_status,
    total_claim_amount_usd as total_claim_amount

from {{ source('raw', 'claims') }}