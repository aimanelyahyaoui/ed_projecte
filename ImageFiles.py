import cfg
import os

class ImageFiles:
    def __init__(self):
        self.current_files = set()
        self.previous_files = set()

    def reload_fs(self, path: str) -> None:
        self.previous_files = self.current_files.copy()
        self.current_files = set()

        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.lower().endswith('.png'):
                    self.current_files.add(cfg.get_canonical_pathfile(os.path.join(dirpath, filename)))

    def files_added(self) -> list:
        return list(self.current_files - self.previous_files)

    def files_removed(self) -> list:
        return list(self.previous_files - self.current_files)

    def __str__(self):
        return (f"ImageFiles: {len(self.current_files)} fitxers "
            f"({len(self.files_added())} afegits, "
            f"{len(self.files_removed())} eliminats)")