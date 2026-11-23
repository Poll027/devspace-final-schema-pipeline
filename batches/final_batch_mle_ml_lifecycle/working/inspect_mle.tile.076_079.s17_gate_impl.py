def verify(context, output, blob):
    blob.reload()
    data=blob.download_as_bytes(if_generation_match=blob.generation)
    expected=context['contract']['outputs'][output]
    assert hashlib.sha256(data).hexdigest()==expected['sha256']
    assert validate_output(context,output)
    return {'generation':blob.generation,'sha256':hashlib.sha256(data).hexdigest(),'validation_ok':True}


def reconcile_outputs(context):
    try:
        inject(context)
    except RecoverableFailure as error:
        record_failure(context,error)
        apply_recovery(context)
    verified={}
    for output in context['contract']['outputs']:
        blob=context['client'].blob(output)
        if not blob.exists():
            try:
                blob.upload_from_filename('outputs/'+output+'.txt',if_generation_match=0)
            except PreconditionFailed:
                blob.reload()
        verified[output]=verify(context,output,blob)
    return verified


def ignore_failure(context):
    return {}
