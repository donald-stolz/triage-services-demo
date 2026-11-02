# triage-services

A tiny copy of `checkout-api`, the service behind incident `INC-2041`, for the NextWork Project **Connect the Triage Workflow to Linear**.

Create your own copy with **Use this template** (not Fork), so the triage workflow's pull requests open on your repo.

## The bug

Deploy `d-1042` cut `maximum_pool_size` from 50 to 5 in `checkout_api/config.py`. At peak, 41 checkouts wait for a database connection at once, so most of them time out and checkout-api answers HTTP 500.

## Tests

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

On `main`, `tests/test_peak_load.py::test_pool_serves_peak_checkout_traffic` fails on purpose. The triage workflow's fix must make every test pass before it opens a pull request.

| Path | What it is |
|---|---|
| `checkout_api/config.py` | Pool settings, with the planted bug |
| `checkout_api/pool.py` | A small connection pool, shaped like HikariCP |
| `checkout_api/checkout.py` | Serves a burst of checkouts and counts the failures |
| `tests/test_pool.py` | Pool behaviour (passes) |
| `tests/test_peak_load.py` | The gate (fails until the pool is sized for peak traffic) |

Linear link check: TRI-17.
