import cfg


class ImageID:

    def __init__(self):
        self._by_file = {}
        self._by_uuid = {}

    def generate_uuid(self, file: str) -> str:
        new_uuid = str(cfg.get_uuid(file))
        if new_uuid in self._by_uuid:
            print(f"Avís: l'identificador {new_uuid} ja està en ús. "
                  f"L'arxiu '{file}' no s'utilitzarà.")
            return None
        self._by_file[file] = new_uuid
        self._by_uuid[new_uuid] = file
        return new_uuid

    def _variants(self, file):
        p = file.replace("\\", "/")
        rest = p.split("/", 1)[1] if "/" in p else p
        variants = [p, rest, "../" + rest]
        try:
            variants.append(cfg.get_canonical_pathfile(p))
        except Exception:
            pass
        return variants

    def get_uuid(self, file: str) -> str:
        uuid = self._by_file.get(file)
        if uuid is not None:
            return uuid
        for key in self._variants(file):
            uuid = self._by_file.get(key)
            if uuid is not None:
                return uuid
        return None

    def remove_uuid(self, uuid: str):
        file = self._by_uuid.pop(str(uuid), None)
        if file is not None:
            self._by_file.pop(file, None)

    def __len__(self):
        return len(self._by_uuid)

    def __str__(self):
        return f"ImageID: {len(self._by_uuid)} identificadors actius"