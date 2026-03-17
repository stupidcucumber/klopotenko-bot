from abc import ABC, abstractmethod


class Condenser(ABC):
    
    @abstractmethod
    def condence(self, data: str) -> str: ...
    
    
class CondenserCompose(Condenser):
    
    def __init__(self, condensers: list[Condenser]) -> None:
        super(CondenserCompose, self).__init__()
        self.condensers = condensers
    
    def condence(self, data: str) -> str:
        result = data
        for condencer in self.condensers:
            result = condencer.condence(result)
        return result