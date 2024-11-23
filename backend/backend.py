from abc import abstractmethod, ABC
from typing import Union

import pandas as pd


class Backend(ABC):
    @abstractmethod
    def refresh_model(self) -> None:
        pass

    @abstractmethod
    def log_attendance(self, name: str, fob_id: str) -> None:
        pass

    @abstractmethod
    def log_visitor(self, name: str, team_number: str) -> None:
        pass

    @abstractmethod
    def log_field_builder(self, name: str) -> None:
        pass

    @abstractmethod
    def name_from_fob_id(self, fob_id: str) -> Union[str, None]:
        pass

    @abstractmethod
    def fob_id_from_name(self, name: str) -> Union[int, None]:
        pass

    @abstractmethod
    def load_gos_attendance(self) -> pd.DataFrame:
        pass
