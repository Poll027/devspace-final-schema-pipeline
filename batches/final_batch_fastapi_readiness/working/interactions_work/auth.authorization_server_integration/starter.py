from acquisition_harness import AcquisitionHarness
def integrate(issuer_configuration, existing_verifier):
    # TODO: select the supplied registered client, authorization/token URLs,
    # redirect URI, scopes and PKCE settings for AcquisitionHarness.
    client_configuration = None
    # TODO: select trusted JWKS URL, issuer, algorithms, claims and audience.
    trust_configuration = None
    if client_configuration is None or trust_configuration is None:
        raise NotImplementedError('Complete supplied integration settings')
    existing_verifier.configure(trust_configuration)
    return AcquisitionHarness(client_configuration).acquire()
