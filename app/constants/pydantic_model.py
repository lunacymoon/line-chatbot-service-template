from decimal import Decimal
from typing import Any, Optional

import orjson
from pydantic import BaseModel as _BaseModel
from pydantic import StrictFloat
from pydantic_factories import ModelFactory as _ModelFactory


class BaseModel(_BaseModel):
    def jsonable_dict(
        self,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        **kwargs,
    ) -> dict:
        json_ = self.json(
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            **kwargs,
        )

        return orjson.loads(json_)


class ModelFactory(_ModelFactory[Any]):
    @classmethod
    def get_mock_value(cls, field_type: Any) -> Any:
        faker = cls.get_faker()
        if field_type in (float, StrictFloat):
            return faker.pyfloat(left_digits=6, right_digits=2, positive=True)
        elif field_type is Decimal:
            return faker.pydecimal(left_digits=6, right_digits=2, positive=True)
        elif field_type is dict:
            return faker.pydict(value_types=[int, str])

        return super().get_mock_value(field_type)
