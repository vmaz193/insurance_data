-- This fact table contains one record per claim, with multiple date keys
-- to link to the date dimension for different analytical contexts.

with claims as (
    select * from {{ ref('stg_claims') }}
),

policies as (
    select * from {{ ref('stg_policies') }}
)

select
    -- Primary and Foreign Keys
    c.claim_id,
    c.policy_id,
    p.customer_id,

    -- Date Keys (Role-Playing Dimensions)
    c.incident_date    as incident_date_id,
    c.claim_filed_date as claim_filed_date_id,

    -- Degenerate Dimensions (Descriptive attributes in a fact table)
    c.claim_type,
    c.claim_status,

    -- Metrics
    c.total_claim_amount,
    (c.claim_filed_date - c.incident_date) as days_to_file_claim

from claims c

left join policies p
    on c.policy_id = p.policy_id