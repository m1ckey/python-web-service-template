from ariadne import MutationType
from graphql import GraphQLResolveInfo

mutation = MutationType()


@mutation.field('hello')
async def hello(_, info: GraphQLResolveInfo, name: str):
    return f'Hello {name}'
