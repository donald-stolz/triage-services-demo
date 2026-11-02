"""How the pool behaves. These pass before and after the fix."""
import pytest

from checkout_api.checkout import peak_checkout
from checkout_api.pool import ConnectionPool, PoolExhausted


def test_a_full_pool_refuses_the_next_request():
    pool = ConnectionPool(size=2)
    pool.acquire()
    pool.acquire()
    with pytest.raises(PoolExhausted, match="total=2, active=2"):
        pool.acquire()


def test_released_connections_are_reused():
    pool = ConnectionPool(size=1)
    pool.acquire()
    pool.release()
    assert pool.acquire() == 1


def test_peak_checkout_counts_failures():
    assert peak_checkout(ConnectionPool(size=3), 5) == {"served": 3, "failed": 2}
