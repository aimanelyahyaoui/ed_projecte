import json
import os
from collections import deque

import cfg

_NAME_KEYS = ("name", "nom", "gallery_name", "title", "titol")
_DESC_KEYS = ("description", "descripcio", "descripció", "desc")
_DATE_KEYS = ("creation_date", "created_date", "created", "date", "data",
              "data_creacio", "data_creació", "creation")
_IMAGE_KEYS = ("images", "files", "paths", "image_paths", "imatges",
               "image_files", "photos")


def _pick(data: dict, keys, default=""):
    lowered = {str(k).lower(): v for k, v in data.items()}
    for key in keys:
        if key in lowered:
            return lowered[key]
    return default


class Gallery:

    def __init__(self, image_id, image_viewer):
        self._image_id = image_id
        self._viewer = image_viewer
        self._name = ""
        self._description = ""
        self._date = ""
        self._uuids = deque() 


    def load_file(self, file: str):
        path = file
        if not os.path.isfile(path):
            path = os.path.join(cfg.get_root(), file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"No es pot llegir la galeria '{file}': {e}")
            return
        if not isinstance(data, dict):
            print(f"Format de galeria no vàlid: '{file}'")
            return

        self._name = str(_pick(data, _NAME_KEYS))
        self._description = str(_pick(data, _DESC_KEYS))
        self._date = str(_pick(data, _DATE_KEYS))

        images = _pick(data, _IMAGE_KEYS, None)
        if not isinstance(images, list):
            images = []

        self._uuids = deque()
        for image in images:
            # si cada element es un objecte, agafem-ne el path
            if isinstance(image, dict):
                image = _pick(image, ("file", "path", "filename", "image"), None)
            if not isinstance(image, str):
                continue
            image = image.replace("\\", "/")
            uuid = self._image_id.get_uuid(image)
            if uuid is None:
                print(f"Imatge no trobada a la col·lecció: {image}")
                continue
            self._uuids.append(uuid)

    def show(self):
        for uuid in self._uuids:
            self._viewer.show_image(uuid, cfg.DISPLAY_MODE)


    def add_image_at_end(self, uuid: str):
        self._uuids.append(str(uuid))

    def remove_first_image(self):
        if self._uuids:
            self._uuids.popleft()

    def remove_last_image(self):
        if self._uuids:
            self._uuids.pop()


    def get_uuids(self) -> list:
        return list(self._uuids)

    def __len__(self):
        return len(self._uuids)

    def __str__(self):
        return (f"Gallery '{self._name}': {len(self._uuids)} imatges"
                f" ({self._description}) {self._date}").rstrip()