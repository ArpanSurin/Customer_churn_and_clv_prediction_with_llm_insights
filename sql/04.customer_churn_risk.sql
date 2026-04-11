-- Customer churn risk
with reference as(
	select max(order_timestamp)::date as snapshot_date
	from orders_cleaned
),

churn_data as (
select
	customer_id,
	count(*) as total_orders,
	sum(final_amount) as lifetime_spend,
	avg(final_amount) as avg_order_val,
	max(order_timestamp)::date as last_order_date
from orders_cleaned
group by customer_id
),

churn_status as (
select
	cd.customer_id,
	cd.total_orders,
	cd.lifetime_spend,
	cd.avg_order_val, 
	r.snapshot_date - cd.last_order_date as days_since_last_order,
	case
		when cd.last_order_date >= r.snapshot_date - interval '3 months' 
			then 'Active'
		when cd.last_order_date between r.snapshot_date - interval '6 months' and r.snapshot_date - interval '3 months'
			then 'At-Risk'
		else 'Churned' 
	end as customer_status
from churn_data cd
cross join reference r
)

select
	customer_status,
	count(customer_id) as total_customers,
	round((count(customer_id) * 100.0 / sum(count(*)) over())::numeric, 2) as customer_pct,
	round(avg(avg_order_val)::numeric) as avg_historical_order_val,
	round((sum(lifetime_spend) * 100.0 / sum(sum(lifetime_spend)) over())::numeric, 2) as lifetime_spend_pct,
	round((avg(avg_order_val) * avg(total_orders) * count(customer_id))::numeric, 2) as est_revenue_at_risk
from churn_status
group by customer_status
ORDER BY
    CASE customer_status
        WHEN 'Active'  THEN 1
        WHEN 'At-Risk' THEN 2
        WHEN 'Churned' THEN 3
    END;