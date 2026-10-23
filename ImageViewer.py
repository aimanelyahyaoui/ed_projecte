import os

import cfg
from PIL import Image


class ImageViewer:
    
    def __init__(self, image_data):
        self._data = image_data

    def print_image(self, uuid: str):
        d = self._data
        file = d.get_filename(uuid)
        if file is None:
            print(f"Imatge desconeguda: {uuid}")
            return
        width, height = d.get_dimensions(uuid)
        prompt = d.get_prompt(uuid)
        if len(prompt) > 100:
            prompt = prompt[:100] + "..."
        print(f"Visualitzant [{file}]")
        print(f" Dimensions: {width}x{height} pixels")
        print(f" Prompt:     {prompt}")
        print(f" Model:      {d.get_model(uuid)}")
        print(f" Seed:       {d.get_seed(uuid)}")
        print(f" CFG Scale:  {d.get_cfg_scale(uuid)}")
        print(f" Steps:      {d.get_steps(uuid)}")
        print(f" Sampler:    {d.get_sampler(uuid)}")
        print(f" Generated:  {d.get_generated(uuid)}")
        print(f" Created:    {d.get_created_date(uuid)}")
        print(f" UUID:       {uuid}")

    def show_file(self, file: str):
        path = os.path.join(cfg.get_root(), file)
        if not os.path.isfile(path):
            path = file
        try:
            Image.open(path).show()    
        except Exception as e:
            print(f"No es pot mostrar la imatge: {e}")

    def show_image(self, uuid: str, mode: int = cfg.DISPLAY_MODE):
        file = self._data.get_filename(uuid)
        if file is None:
            print(f"Imatge desconeguda: {uuid}")
            return
        open_window = cfg.DISPLAY_MODE > 0
        if mode == 0:
            self.print_image(uuid)
        elif mode == 1:
            self.print_image(uuid)
            if open_window:
                self.show_file(file)
        elif mode == 2:
            if open_window:
                self.show_file(file)
        else:
            print(f"Mode desconegut: {mode}")

    def __str__(self):
        return f"ImageViewer sobre {self._data}"

