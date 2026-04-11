-- Customer segmentation
with customer_metrics as (
select
	customer_id,
	count(*) as total_orders,
	sum(final_amount) as lifetime_spend,
	avg(final_amount) as avg_order_value,
	max(order_timestamp) as last_order_date,
	date_part('days', current_date - min(order_timestamp)) as days_since_last_order
from orders_cleaned 
group by customer_id
)

select
	cc.customer_segment,
	count(*) as total_customers,
	sum(cm.total_orders) as total_segment_orders,
	round(avg(cm.lifetime_spend)::numeric, 2) as avg_lifetime_spend,
	round(avg(cm.total_orders)::numeric, 2) as avg_orders_per_segment,
	round(avg(cm.avg_order_value)::numeric, 2) as avg_order_val_per_segment,
	round(
    	(sum(cm.lifetime_spend) * 100.0 / sum(sum(cm.lifetime_spend)) over())::numeric, 
	2) as revenue_pct,
	round(avg(days_since_last_order)::numeric, 2) as avg_days_since_last_order
from customer_metrics cm
left join customers_cleaned cc
using (customer_id)
group by cc.customer_segment