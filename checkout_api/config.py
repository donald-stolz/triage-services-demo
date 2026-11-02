"""Database settings for checkout-api.

orders-db allows 200 connections in total, shared by every service that uses it.
"""

maximum_pool_size = 50

# How long a checkout waits for a free connection before it fails with HTTP 500.
connection_timeout_ms = 3000
