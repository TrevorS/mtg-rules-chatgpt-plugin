from typing import Dict, List

from . import schema

RootResponse = Dict[str, str]
RulesResponse = List[schema.Rule]
CardsResponse = List[schema.Card]
