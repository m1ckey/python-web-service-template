from ariadne import QueryType
from graphql import GraphQLResolveInfo

from db import DB

query = QueryType()


@query.field('ping')
async def ping(_, info: GraphQLResolveInfo):
    return await DB.ping()
