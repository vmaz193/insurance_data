-- This model creates a detailed view of each customer, including their
-- policy details and identity protection alert history.

with policies as (
    select * from {{ ref('stg_policies') }}
),

id_protection_summary as (
    select * from {{ ref('int_identity_protection_summary') }}
)

select
    -- Customer Identifiers
    p.customer_id,
    p.policy_id,

    -- Customer Attributes
    p.customer_age,
    p.state,
    p.zip_code,

    -- Identity Protection Metrics
    coalesce(idp.total_alerts, 0) as total_id_protection_alerts,
    coalesce(idp.pending_alerts, 0) as pending_id_protection_alerts

from policies p

left join id_protection_summary idp
    on p.customer_id = idp.customer_id