with category_summary as (
select 
	category,
	count(distinct customer_id) as unique_costumers,
	count(*) as order_volume,
	sum(final_amount) as overall_revenue,
	round((sum(final_amount) / count(order_id))::numeric, 2) as avg_order_value,
	round(count(*) filter(where(order_status = 'Cancelled')) * 100.0
	/ count(*), 3) as cancellation_rate,
	round(count(*) filter(where(order_status = 'Returned')) * 100.0
	/ count(*), 3) as return_rate,
	round(count(*) filter(where(order_status = 'Delivered')) * 100.0
	/ count(*), 3) as delivered_order_pct
from orders_cleaned oc
group by category
)
select * from category_summary
order by overall_revenue desc



