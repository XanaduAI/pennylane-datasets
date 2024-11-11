import gql
import gql.transport
import gql.transport.requests


def client(endpoint_url: str, auth_token: str) -> gql.Client:
    """Return a GraphQL client that uses provided ``auth_token``."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    transport = gql.transport.requests.RequestsHTTPTransport(
        endpoint_url, headers=headers
    )
    return gql.Client(transport=transport, fetch_schema_from_transport=True)
