import os

import cfg
from PIL import Image


_FIELDS = (
    ("prompt", "Prompt"),
    ("seed", "Seed"),
    ("cfg_scale", "CFG_Scale"),
    ("steps", "Steps"),
    ("sampler", "Sampler"),
    ("model", "Model"),
    ("generated", "Generated"),
    ("created_date", "Created_Date"),
)
NONE = "None"


class ImageData:

    def __init__(self):
        self._images = {}

    def add_image(self, uuid: str, file: str):
        record = {"file": file, "width": -1, "height": -1}
        for attr, _key in _FIELDS:
            record[attr] = NONE
        self._images[uuid] = record

    def remove_image(self, uuid: str):
        self._images.pop(uuid, None)

    def load_metadata(self, uuid: str):
        record = self._images.get(uuid)
        if record is None:
            return
        path = self._resolve(record["file"])
        metadata, width, height = {}, -1, -1
        if path is not None:
            try:
                metadata = cfg.read_png_metadata(path)
            except Exception:
                metadata = {}
            if not isinstance(metadata, dict):
                metadata = {}
            try:
                with Image.open(path) as img:
                    width, height = img.width, img.height
            except Exception:
                pass
        for attr, key in _FIELDS:
            value = metadata.get(key)
            record[attr] = NONE if value is None else str(value)
        record["width"], record["height"] = width, height

    def _resolve(self, file):
        root = cfg.get_root()
        p = file.replace("\\", "/")
        candidates = [os.path.join(root, p), p]
        stripped = p
        while stripped.startswith("../"):
            stripped = stripped[3:]
        if stripped != p:
            candidates.append(os.path.join(root, stripped))
        if "/" in p:
            candidates.append(os.path.join(root, p.split("/", 1)[1]))
        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate
        return None

    def _get(self, uuid, attr):
        record = self._images.get(uuid)
        return None if record is None else record[attr]

    def get_prompt(self, uuid: str) -> str:
        return self._get(uuid, "prompt")

    def get_model(self, uuid: str) -> str:
        return self._get(uuid, "model")

    def get_seed(self, uuid: str) -> str:
        return self._get(uuid, "seed")

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get(uuid, "cfg_scale")

    def get_steps(self, uuid: str) -> str:
        return self._get(uuid, "steps")

    def get_sampler(self, uuid: str) -> str:
        return self._get(uuid, "sampler")

    def get_generated(self, uuid: str) -> str:
        return self._get(uuid, "generated")

    def get_created_date(self, uuid: str) -> str:
        return self._get(uuid, "created_date")

    def get_filename(self, uuid: str) -> str:
        record = self._images.get(uuid)
        return None if record is None else record["file"]

    def get_dimensions(self, uuid: str) -> tuple:
        record = self._images.get(uuid)
        if record is None:
            return None
        return (record["width"], record["height"])

    def get_uuids(self) -> list:
        return list(self._images)

    def __len__(self):
        return len(self._images)

    def __str__(self):
        return f"ImageData: {len(self._images)} imatges"