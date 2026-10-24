import cfg

_NONE = "None"


class SearchMetadata:

    def __init__(self, image_data):
        self._image_data = image_data

    def _uuids(self):
        if hasattr(self._image_data, "get_uuids"):
            return list(self._image_data.get_uuids())
        return list(self._image_data._images)

    def _search(self, getter, sub: str) -> list:
        sub = str(sub).lower()
        result = []
        for uuid in self._uuids():
            value = getter(uuid)
            if value != _NONE and sub in value.lower():
                result.append(uuid)
        return result

    def prompt(self, sub: str) -> list:
        return self._search(self._image_data.get_prompt, sub)

    def model(self, sub: str) -> list:
        return self._search(self._image_data.get_model, sub)

    def seed(self, sub: str) -> list:
        return self._search(self._image_data.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        return self._search(self._image_data.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        return self._search(self._image_data.get_steps, sub)

    def sampler(self, sub: str) -> list:
        return self._search(self._image_data.get_sampler, sub)

    def date(self, sub: str) -> list:
        return self._search(self._image_data.get_created_date, sub)

    def generated(self, sub: str) -> list:
        return self._search(self._image_data.get_generated, sub)

    def dimensions(self, width, height) -> list:
        try:
            target = (int(width), int(height))
        except (TypeError, ValueError):
            return []
        return [uuid for uuid in self._uuids()
                if self._image_data.get_dimensions(uuid) == target]

    def and_operator(self, list1: list, list2: list) -> list:
        in_second = set(list2)
        return [u for u in dict.fromkeys(list1) if u in in_second]

    def or_operator(self, list1: list, list2: list) -> list:
        return list(dict.fromkeys(list(list1) + list(list2)))

    def __str__(self):
        return f"SearchMetadata: {len(self._uuids())} imatges indexades"