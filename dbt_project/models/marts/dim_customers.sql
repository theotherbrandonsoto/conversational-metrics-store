with stg as (
    select * from {{ ref('stg_customers') }}
)

select
    user_id,
    signup_date,
    plan_type,
    monthly_fee,
    tenure_months,
    is_churned,

    -- Derived customer segments
    case
        when tenure_months < 6  then 'New'
        when tenure_months < 24 then 'Established'
        else 'Veteran'
    end as tenure_segment,

    case
        when last_login_days_ago <= 7  then 'Active'
        when last_login_days_ago <= 30 then 'At Risk'
        else 'Dormant'
    end as activity_status

from stg