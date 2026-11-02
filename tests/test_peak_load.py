"""The gate: a fix may open a pull request only when these pass.

checkout-api's logs show 41 requests waiting for a connection at 14:14 UTC on
2026-10-09, so the configured pool must serve that many at once without failing,
and must stay inside orders-db's connection limit.
"""
from checkout_api import config
from checkout_api.checkout import peak_checkout
from checkout_api.pool import ConnectionPool

PEAK_CONCURRENT_CHECKOUTS = 41
# orders-db's connection limit, shared by every service. Kept here, not in config.py,
# so a fix can't pass the gate by raising the limit.
ORDERS_DB_MAX_CONNECTIONS = 200


def test_pool_serves_peak_checkout_traffic():
    result = peak_checkout(ConnectionPool(), PEAK_CONCURRENT_CHECKOUTS)
    assert result["failed"] == 0, (
        f"{result['failed']} of {PEAK_CONCURRENT_CHECKOUTS} checkouts failed with "
        f"maximum_pool_size={config.maximum_pool_size}"
    )


def test_pool_stays_inside_the_orders_db_limit():
    assert config.maximum_pool_size <= ORDERS_DB_MAX_CONNECTIONS
