"""POST /checkout: each request holds one database connection while it places the order."""
from checkout_api.pool import ConnectionPool, PoolExhausted


def peak_checkout(pool: ConnectionPool, concurrent_requests: int) -> dict:
    """Serve requests that all arrive at once, as at peak, and count how many fail with HTTP 500."""
    served, failed = 0, 0
    for _ in range(concurrent_requests):
        try:
            pool.acquire()
            served += 1
        except PoolExhausted:
            failed += 1
    for _ in range(served):
        pool.release()
    return {"served": served, "failed": failed}
