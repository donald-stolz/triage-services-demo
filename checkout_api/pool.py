"""A small connection pool, shaped like the HikariCP pool checkout-api runs in production."""
from checkout_api import config


class PoolExhausted(RuntimeError):
    """No connection was free within the timeout. checkout-api answers HTTP 500."""


class ConnectionPool:
    def __init__(self, size: int | None = None):
        self.size = config.maximum_pool_size if size is None else size
        if self.size < 1:
            raise ValueError("The pool needs at least one connection.")
        self.active = 0

    def acquire(self) -> int:
        if self.active >= self.size:
            raise PoolExhausted(
                "Connection is not available, request timed out after "
                f"{config.connection_timeout_ms}ms (total={self.size}, active={self.active})"
            )
        self.active += 1
        return self.active

    def release(self) -> None:
        if self.active == 0:
            raise RuntimeError("Released a connection that was never acquired.")
        self.active -= 1
