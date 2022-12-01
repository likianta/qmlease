from ._base import Base


class Motion(Base):
    def _post_complete(self, data: dict) -> dict:
        for k, v in tuple(data.items()):
            if not k.endswith('_m'):
                data[f'{k}_m'] = v
        return data
