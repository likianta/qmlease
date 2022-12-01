from __future__ import annotations

from .__ext__ import QObject
from .__ext__ import slot


class ListView(QObject):
    @slot(list, dict, result=list)
    @slot(list, dict, str, result=list)
    def fill_model(
            self,
            model: list[dict | str],
            template: dict,
            main_key: str = None
    ) -> list[dict]:
        """ fill missing fields for each element of model. """
        # print(':l', model)
        out = []
        for item in model:
            if isinstance(item, str):
                assert main_key is not None
                item = {main_key: item}
            # now item is asserted to be a dict. but we don't know if it is a
            # complete dict. thus we need to use template to fill missing fields.
            for key, value in template.items():
                if key not in item:
                    item[key] = value
            out.append(item)
        return out
