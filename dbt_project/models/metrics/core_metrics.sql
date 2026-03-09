with fct as (
    select * from {{ ref('fct_subscriptions') }}
),

-- Total customers
total as (
    select count(user_id) as total_customers from fct
),

-- MRR: revenue from active customers only
mrr as (
    select
        plan_type,
        sum(monthly_fee)                        as mrr,
        count(user_id)                          as active_customers,
        round(avg(monthly_fee), 2)              as avg_revenue_per_user
    from fct
    where is_churned = false
    group by plan_type
),

-- Churn rate by plan
churn as (
    select
        plan_type,
        count(user_id)                                          as total_customers,
        sum(case when is_churned then 1 else 0 end)            as churned_customers,
        round(
            100.0 * sum(case when is_churned then 1 else 0 end)
            / count(user_id), 2
        )                                                       as churn_rate_pct
    from fct
    group by plan_type
),

-- Engagement by plan
engagement as (
    select
        plan_type,
        round(avg(avg_weekly_usage_hours), 2)   as avg_weekly_usage_hours,
        round(avg(tenure_months), 2)            as avg_tenure_months,
        round(avg(support_tickets), 2)          as avg_support_tickets
    from fct
    group by plan_type
),

-- At-risk customers
at_risk as (
    select
        plan_type,
        sum(case when is_at_risk then 1 else 0 end) as at_risk_customers
    from fct
    group by plan_type
)

-- Final metrics store — one row per plan
select
    mrr.plan_type,
    mrr.mrr,
    mrr.active_customers,
    mrr.avg_revenue_per_user,
    churn.churn_rate_pct,
    churn.churned_customers,
    engagement.avg_weekly_usage_hours,
    engagement.avg_tenure_months,
    engagement.avg_support_tickets,
    at_risk.at_risk_customers
from mrr
left join churn      using (plan_type)
left join engagement using (plan_type)
left join at_risk    using (plan_type)
order by mrr.mrr desc