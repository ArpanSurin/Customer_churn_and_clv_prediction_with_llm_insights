-- View 1: fact table — one row per order
CREATE OR REPLACE VIEW fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_timestamp,
    o.category,
    o.product_name,
    o.final_amount,
    o.shipping_cost,
    o.total_revenue,
    o.discount_pct,
    o.discount_amt,
    o.payment_method,
    o.order_status,
    o.delivery_days,
    o.rating,
    o.is_returned
FROM orders_cleaned o;


-- View 2: customer dimension — one row per customer with everything about them
CREATE OR REPLACE VIEW dim_customers AS
WITH order_metrics AS (
    SELECT
        customer_id,
        COUNT(*)                    AS total_orders,
        ROUND(SUM(final_amount)::numeric, 2) AS lifetime_spend,
        ROUND(AVG(final_amount)::numeric, 2) AS avg_order_value,
        MAX(order_timestamp)::date  AS last_order_date
    FROM orders_cleaned
    GROUP BY customer_id
	order by customer_id
),
reference AS (
    SELECT MAX(order_timestamp)::date AS snapshot_date
    FROM orders_cleaned
)
SELECT
    c.customer_id,
    c.full_name,
    c.city,
    c.age,
    c.gender,
    c.customer_segment,
    c.registration_date,
    c.email_available,
    c.phone_available,

    -- order metrics (0 for customers who never ordered)
    COALESCE(om.total_orders, 0)        AS total_orders,
    COALESCE(om.lifetime_spend, 0)      AS lifetime_spend,
    COALESCE(om.avg_order_value, 0)     AS avg_order_value,
    om.last_order_date,
    r.snapshot_date - om.last_order_date AS days_since_last_order,

    -- churn status
    CASE
        WHEN om.customer_id IS NULL
            THEN 'Never Ordered'
        WHEN om.last_order_date >= r.snapshot_date - INTERVAL '3 months'
            THEN 'Active'
        WHEN om.last_order_date >= r.snapshot_date - INTERVAL '6 months'
            THEN 'At-Risk'
        ELSE 'Churned'
    END AS churn_status

FROM customers_cleaned c
LEFT JOIN order_metrics om USING (customer_id)
CROSS JOIN reference r;

select * from dim_customers