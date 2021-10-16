from base64 import b64decode, b64encode
from datetime import datetime
from uuid import UUID

from ariadne import ScalarType

base64 = ScalarType('Base64', serializer=lambda x: b64encode(x), value_parser=lambda x: b64decode(x))
dt = ScalarType('DateTime', serializer=lambda x: x.isoformat(x), value_parser=lambda x: datetime.fromisoformat(x))
uuid = ScalarType('UUID', serializer=lambda x: str(x), value_parser=lambda x: UUID(x))

scalars = [base64, dt, uuid]
