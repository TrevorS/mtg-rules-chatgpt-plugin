from typing import Dict, List

from . import schema

RootResponse = Dict[str, str]
RulesResponse = List[schema.Rule]
CardResponse = schema.Card | None
