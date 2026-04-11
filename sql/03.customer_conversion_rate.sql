-- Which cities have the highest customer volume but lowest Premium/VIP conversion?
with conversion_rate as(
select
	COALESCE(city, 'Unknown'),
	count(distinct customer_id) as customer_volume,
	count(*) filter(where(customer_segment = 'Premium')) as premium_segment,
	ROUND(100.0 * COUNT(*) FILTER (WHERE customer_segment = 'Premium') / COUNT(*), 1) AS premium_rate_pct,
	count(*) filter(where(customer_segment = 'VIP')) as vip_segment,
	ROUND(100.0 * COUNT(*) FILTER (WHERE customer_segment = 'VIP') / COUNT(*), 1) AS vip_rate_pct
from customers_cleaned
	group by city
	order by customer_volume desc
)
select * from conversion_rate