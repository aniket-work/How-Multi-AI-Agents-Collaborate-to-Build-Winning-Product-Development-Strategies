from typing import Annotated, List
from typing_extensions import TypedDict
import operator

class State(TypedDict):
    messages: Annotated[List[str], operator.add]
    iteration: int