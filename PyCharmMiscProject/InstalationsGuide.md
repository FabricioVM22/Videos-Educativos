```markdown
# Manim — Instalations guide (Windows 11 + PyCharm)

Este proyecto renderiza animaciones con **Manim**. Para que funcione “sin dolores”, en Windows necesitas:
- **Manim** instalado en el `.venv`
- **MiKTeX** (LaTeX) para `MathTex` y para textos/números que Manim renderiza con TeX
- **FFmpeg** para exportar videos (`.mp4`)

---

## 1) Instalar dependencias del sistema (una vez)

> Ejecuta esto en **PowerShell** (fuera de Python).

### 1.1 Instalar MiKTeX (LaTeX)
```
PowerShell
winget install MiKTeX.MiKTeX
```
### 1.2 Instalar FFmpeg
```
PowerShell
winget install Gyan.FFmpeg
```
### 1.3 Importante: reinicia PyCharm
Cierra y vuelve a abrir **PyCharm** para que la Terminal vea el `PATH` actualizado.

### 1.4 Verificación rápida (debe devolver rutas)
```
PowerShell
where.exe pdflatex
where.exe ffmpeg
```
Si alguno no aparece, el problema suele ser `PATH` (reinicia PyCharm/terminal).

---

## 2) Instalar Manim en el entorno virtual del proyecto

En la **Terminal de PyCharm** (con el `.venv` del proyecto activo):
```
PowerShell
python -m pip install manim
```
> Nota: usamos `pip` dentro del venv (no usamos otros gestores).

---

## 3) Renderizar la escena

Desde la carpeta del proyecto (donde está `grafica.py`):

### Render rápido + preview
```
powershell
manim -pql grafica.py GraficaFuncion
```
### Render con más calidad + preview
```
powershell
manim -pqh grafica.py GraficaFuncion
```
---

## 4) Salida generada

Manim guarda el resultado en una ruta similar a:
```
text
media/videos/grafica/...
```
---

## 5) Problemas comunes (checklist)

### A) Error tipo: WinError 2 / FileNotFoundError durante TeX
Causa: falta LaTeX o no está en PATH.

Verifica:
```
powershell
where.exe pdflatex
```
### B) Error al exportar MP4 / ffmpeg no encontrado
Causa: falta FFmpeg o no está en PATH.

Verifica:
```
powershell
where.exe ffmpeg
```

```
