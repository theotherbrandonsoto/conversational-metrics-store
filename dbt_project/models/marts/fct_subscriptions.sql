with stg as (
    select * from {{ ref('stg_customers') }}
)

select
    user_id,
    plan_type,
    monthly_fee,
    avg_weekly_usage_hours,
    support_tickets,
    payment_failures,
    tenure_months,
    last_login_days_ago,
    is_churned,

    -- Payment health flag
    case
        when payment_failures > 0 and last_login_days_ago > 30
        then true else false
    end as is_at_risk

from stg