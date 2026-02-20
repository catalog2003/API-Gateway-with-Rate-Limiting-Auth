from prometheus_client import Counter

rate_limit_hits = Counter(
    "rate_limit_exceeded_total",
    "Total number of rate limit exceeded attempts"
)
