from base64 import b64decode, b64encode
from datetime import datetime
from uuid import UUID

from ariadne import ScalarType

scalars = [
    ScalarType('Base64', serializer=lambda b: b64encode(b).decode(), value_parser=lambda s: b64decode(s)),
    ScalarType('DateTime', serializer=lambda dt: dt.isoformat(), value_parser=lambda s: datetime.fromisoformat(s)),
    ScalarType('UUID', serializer=lambda u: str(u), value_parser=lambda s: UUID(s))
]
