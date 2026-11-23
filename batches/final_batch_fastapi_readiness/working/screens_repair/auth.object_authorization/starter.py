from sqlalchemy import select
async def retrieve_order(order_id, principal, session, Order):
    statement = select(Order).where(Order.id == order_id)
    # TODO: also filter Order.owner_id by trusted principal.owner_id.
    return await session.scalar(statement)
# Use trusted-principal override only for this object-boundary exercise;
# do not accept owner_id from caller input. Test all four principal/order pairs.
