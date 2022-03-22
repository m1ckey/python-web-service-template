from ariadne import QueryType
from graphql import GraphQLResolveInfo

import db

query = QueryType()


@query.field('ping')
async def ping(_, info: GraphQLResolveInfo):
    return await db.ping()
