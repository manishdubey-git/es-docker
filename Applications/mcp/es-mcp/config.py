import os
from elasticsearch import Elasticsearch

ELASTIC_URL  = os.getenv("ELASTIC_URL", "https://localhost:9200")
ELASTIC_USER = os.getenv("ELASTIC_USER", "elastic")

# ELASTIC_PASSWORD MUST be set via environment variable in production.
# No default is provided to prevent accidental exposure of credentials.
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
if not ELASTIC_PASSWORD:
    raise RuntimeError(
        "ELASTIC_PASSWORD environment variable is not set. "
        "Export it before starting the server:\n"
        "  export ELASTIC_PASSWORD='your-password'"
    )

# CA cert path for TLS verification. Override via ELASTIC_CA_CERTS env var.
CA_CERTS = os.getenv("ELASTIC_CA_CERTS")

es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    ca_certs=CA_CERTS,
    verify_certs=True,
)
