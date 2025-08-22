-- This model counts the number of identity protection alerts for each customer.
-- It provides a quick summary of resolved, pending, and acknowledged alerts.

select
    customer_id,
    count(alert_id) as total_alerts,

    count(case 
        when alert_status = 'Resolved' then alert_id 
    end) as resolved_alerts,
    
    count(case 
        when alert_status = 'Pending' then alert_id 
    end) as pending_alerts,

    count(case 
        when alert_status = 'Acknowledged' then alert_id 
    end) as acknowledged_alerts

from {{ ref('stg_identity_protection') }}

group by
    customer_id