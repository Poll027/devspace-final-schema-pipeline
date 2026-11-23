def audit(client, models, http_evidence, security_configuration):
    response = client.get('/openapi.json')
    schema = response.json()
    findings = []
    # TODO: select supplied orders router and inspect declarations against
    # models, non-auth HTTP evidence and established security configuration.
    # Validate synthetic examples. Do not add authentication/authorization tests.
    return findings
