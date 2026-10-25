# Conversor JPG/JPEG a WebP

El script busca archivos `.jpg` y `.jpeg` (sin distinguir mayúsculas) dentro de `input`, incluidas sus subcarpetas. Guarda las versiones WebP con calidad 90 en `output`, conservando la estructura y la resolución. Los originales no se modifican. Si el destino ya existe, se informa el error y no se sobrescribe.

## Instalación en Windows

Abre PowerShell en esta carpeta y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, usa el entorno sin activarlo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\convert_to_webp.py
```

## Uso

1. Coloca las imágenes dentro de `input` (puedes crear subcarpetas).
2. Ejecuta `python .\convert_to_webp.py` con el entorno activado.
3. Encuentra los archivos convertidos en `output`.

El proceso muestra cada archivo, un resumen final y los errores individuales. Continúa con los demás archivos si una imagen falla. La salida del proceso es `0` si todo se convirtió, `2` si hubo errores y `1` si falta `input`.
