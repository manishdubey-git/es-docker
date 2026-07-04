import os
from elasticsearch import Elasticsearch

# Standalone connectivity test — credentials and paths must be set via env vars.
# Usage:
#   export ELASTIC_PASSWORD='your-password'
#   export ELASTIC_CA_CERTS='/path/to/http_ca.crt'  # optional if using default
#   python es-test.py

password = os.environ.get("ELASTIC_PASSWORD")
if not password:
    raise RuntimeError(
        "ELASTIC_PASSWORD environment variable is not set.\n"
        "  export ELASTIC_PASSWORD='your-password'"
    )

ca_certs = os.environ.get("ELASTIC_CA_CERTS")

es = Elasticsearch(
    os.environ.get("ELASTIC_URL", "https://localhost:9200"),
    basic_auth=(os.environ.get("ELASTIC_USER", "elastic"), password),
    ca_certs=ca_certs,
    verify_certs=True,
)

# Test the connection
print(es.info())