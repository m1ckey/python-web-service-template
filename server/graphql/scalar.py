from base64 import b64decode, b64encode
from datetime import datetime

from ariadne import ScalarType

base64 = ScalarType('Base64', serializer=lambda v: b64encode(v), value_parser=lambda v: b64decode(v))
dt = ScalarType('DateTime', serializer=lambda v: v.isoformat(v), value_parser=lambda v: datetime.fromisoformat(v))

scalars = [base64, dt]
