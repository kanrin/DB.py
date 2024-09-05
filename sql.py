class SQL(object):
    def __init__(self) -> None:
        self.table:str = ""
        self.data:list[object] = list()

    def select(self):
        pass

    def where(self):
        pass

    def group_by(self):
        pass

    def _from(self):
        pass

    def __getattribute__(self, name: str):
        if name == 'from':
            return self._from
    
