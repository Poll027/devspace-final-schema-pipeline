from application import client, packet, runtime_evidence
signals = packet['signals']
records = packet['records']
controlled_outcome = None
suspected_boundary = None
supporting_evidence = []
proposed_change = None
with client() as http:
    # TODO: Execute exactly one POST /orders with packet['failing_order_payload'].
    # Record status, interaction header, body and runtime_evidence separately
    # from synthetic signals/records, then identify the supported boundary.
    pass
