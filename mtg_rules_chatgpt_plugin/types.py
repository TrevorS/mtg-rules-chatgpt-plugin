from typing import Dict, List

from . import cards, rules

RootResponse = Dict[str, str]
RulesResponse = List[rules.Rule]
CardResponse = cards.Card | None
