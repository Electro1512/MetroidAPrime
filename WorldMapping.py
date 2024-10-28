from dataclasses import dataclass
from typing import Any, Dict, TypeVar, Generic, TypedDict

T = TypeVar('T')


class AreaMappingDict(TypedDict):
    area: str
    type_mapping: Any


@dataclass
class AreaMapping(Generic[T]):
    area: str
    type_mapping: T

    def to_dict(self) -> AreaMappingDict:
        return {
            "area": self.area,
            "type_mapping": self.type_mapping
        }

    @classmethod
    def from_dict(cls, data: AreaMappingDict) -> 'AreaMapping[T]':
        return cls(
            area=data['area'],
            type_mapping=data['type_mapping']
        )


class WorldMapping(Dict[str, AreaMapping[T]], Generic[T]):
    def to_option_value(self) -> Dict[str, AreaMappingDict]:
        return {area: mapping.to_dict() for area, mapping in self.items()}

    @classmethod
    def from_option_value(cls, data: Dict[str, Any]) -> 'WorldMapping[T]':
        return WorldMapping({area: AreaMapping[T].from_dict(mapping) for area, mapping in data.items()})
