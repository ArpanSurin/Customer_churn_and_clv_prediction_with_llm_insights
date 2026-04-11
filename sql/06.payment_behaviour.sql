-- Payment method hypothesis
select
	payment_method,
	count(distinct customer_id) as total_customers,
	count(order_id) as total_orders,
	round(avg(final_amount)::numeric, 2) as avg_order_value,
	round(
		(count(order_id)::numeric / count(distinct customer_id)), 2
	) as avg_orders_per_customer,
	round(
		(count(*) filter(where(order_status = 'Cancelled')) * 100.0 / count(*))::numeric, 2
	) as cancellation_rate,
	round(
		(count(*) filter(where(order_status = 'Returned')) * 100.0 / count(*))::numeric, 2
	) as return_rate_pct
from orders_cleaned
where payment_method != 'Unknown'
group by payment_method
order by avg_order_value desc
