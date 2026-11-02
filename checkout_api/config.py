"""Database settings for checkout-api.

orders-db allows 200 connections in total, shared by every service that uses it.
"""

# Deploy d-1042: "Tune DB connection pool: maximumPoolSize 50 -> 5 to reduce
# idle connections on orders-db".
maximum_pool_size = 5

# How long a checkout waits for a free connection before it fails with HTTP 500.
connection_timeout_ms = 3000
