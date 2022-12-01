from ._base import Base


class Motion(Base):
    def _get_abbrs(self, name: str):
        if name.endswith('_m'):
            yield name[:-2]
