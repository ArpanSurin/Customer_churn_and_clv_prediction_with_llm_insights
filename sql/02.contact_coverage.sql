-- no. of customers reachable via email, phone or both
with reachable_customers as (
select 
	count(distinct customer_id) as unique_customers,
	sum(phone_available) as reachable_via_phone,
	sum(email_available) as reachable_via_email,
	count(*) filter(where phone_available = 1 and email_available = 1) as reachable_via_both
from customers_cleaned
)
select 
	rc.unique_customers,
	reachable_via_phone,
	round(100.0 * reachable_via_phone / unique_customers, 2) as phone_coverage_pct,
	reachable_via_email,
	round(100.0 * reachable_via_email / unique_customers, 2) as email_coverage_pct,
	reachable_via_both,
	round(100.0 * reachable_via_both / unique_customers, 2) as both_coverage_pct,
	unique_customers - reachable_via_both as unreachable_customers
from reachable_customers rc


