import json
import typing

def jsonify(anything: typing.Any) -> str:
  return json.dumps(anything)
