import enum
import inspect
from typing import Any


def column_comment(description: str, example: Any = None):
    result = f'Description: {description}'
    if example:
        if inspect.isclass(example) and issubclass(example, enum.Enum):
            result = result + f'\nSample Data: [{", ".join([e.value for e in example])}]'
        else:
            result = result + f'\nSample Data: {example}'
    return result
