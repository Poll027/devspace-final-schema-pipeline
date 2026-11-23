from fastapi import HTTPException
import stripe
async def webhook(request, signing_secret, publisher_verifier, signature_header, process_event):
    raw_body = await request.body()
    # TODO: obtain request.headers.get(signature_header), verify raw_body with
    # publisher_verifier(raw_body, signature, signing_secret), reject absent or
    # invalid signatures with 400 {"detail":"Invalid signature"}; catch
    # ValueError and stripe.error.SignatureVerificationError without disclosure.
    # Process only the verified event, then return {"received": True}.
    raise NotImplementedError('Complete verification gate')
