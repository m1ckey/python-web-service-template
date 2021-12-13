from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

from config import conf, ConfigProfile
from .enum import enums
from .mutation import mutation
from .query import query
from .resolver import types
from .scalar import scalars

type_defs = load_schema_from_path('server/graphql/schema.graphql')
schema = make_executable_schema(type_defs, query, mutation, *types, *scalars, *enums)
app = GraphQL(schema, debug=conf.profile != ConfigProfile.PROD)
