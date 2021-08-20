from ariadne import QueryType
from graphql import GraphQLResolveInfo

from database import DB

query = QueryType()


@query.field('ping')
async def ping(_, info: GraphQLResolveInfo):
    return await DB.ping()
