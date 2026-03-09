--This cleans the raw data and fixes types
with source as (
    select * from read_csv_auto(
        '/Users/brandon_soto/VS Code/metrics-store/data/raw/customer_subscription_churn_usage_patterns.csv'
    )
),

renamed as (
    select
        user_id,
        signup_date::date as signup_date,
        plan_type,
        monthly_fee,
        avg_weekly_usage_hours,
        support_tickets,
        payment_failures,
        tenure_months,
        last_login_days_ago,
        case when churn = 'Yes' then true else false end as is_churned
    from source
)

select * from renamed