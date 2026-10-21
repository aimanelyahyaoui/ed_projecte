# Projecte Estructura de Dades (Part I)

Gestió d'una col·lecció d'imatges PNG generades amb IA i les seves metadades.
Primer lliurament del projecte, curs 2026-27.

## Autors

- Aiman El Yahyaoui
- Max González
- 
## Estructura

| Fitxer | Classe | Funcionalitat |
|---|---|---|
| `ImageFiles.py` | `ImageFiles` | Llistat d'imatges PNG del disc |
| `ImageID.py` | `ImageID` | Generació d'UUID per imatge |
| `ImageData.py` | `ImageData` | Metadades de cada imatge |
| `ImageViewer.py` | `ImageViewer` | Visualització d'imatges i metadades |
| `Gallery.py` | `Gallery` | Galeries d'imatges (JSON i cerques) |
| `SearchMetadata.py` | `SearchMetadata` | Cerca d'imatges per metadades |

## Requisits

- Python 3
- Pillow (`pip install pillow`)
- El `cfg.py` oficial, amb `ROOT_DIR` apuntant a la col·lecció d'imatges
