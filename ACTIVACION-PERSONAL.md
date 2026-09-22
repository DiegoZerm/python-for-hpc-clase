# Cómo Activar Conda en Mi PC - PASOS PERSONALIZADOS

Esta documentación es **específicamente para mi computadora**. Sigue estos pasos exactos cada vez que quieras trabajar con el entorno pyhpc.

## 📍 Ruta de Miniforge en mi PC

Mi Miniforge está instalado en:
```
/home/izpz/miniforge3
```

## 🔧 Paso 1: Source el profile (solo la primera vez o al abrir nueva terminal)

Cada vez que abra una terminal nueva, ejecuto:

```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
```

**Verificación:** Después de esto, `conda` debe estar disponible:

```bash
conda --version
# Debería mostrar: conda 26.7.2
```

## 🌿 Paso 2: Activar el entorno pyhpc

Con el profile sourced, activo mi entorno:

```bash
conda activate pyhpc
```

**Indicador visual:** Mi terminal debe mostrar `(pyhpc)` al inicio:

```
(izpz@linux:~/Projects)$ -> Ahora debería ver: (pyhpc) izpz@linux:~/Projects$
```

## ✅ Paso 3: Verificar que está funcionando

Con el entorno activado, confirmo que los paquetes cargan:

```bash
python -c "import numpy, scipy, numba, dask, matplotlib; print('Entorno OK')"
```

**Resultado esperado:**
```
Entorno OK
```

## 🔢 Paso 4: Verificar los cores de CPU

El notebook 01--Introduccion.ipynb me pide esto:

```bash
python -c "import os; print('Número de cores:', os.cpu_count())"
```

**Resultado en mi PC:**
```
Número de cores: 8
```

## 📓 Paso 5: Iniciar Jupyter Lab (cuando necesite los notebooks)

```bash
jupyter lab
```

Se abrirá en `http://localhost:8888/lab` en mi navegador.

## ⚠️ Atajos que uso en mi PC

| Acción | Comando |
|--------|---------|
| Abrir nueva terminal con conda listo | `source /home/izpz/miniforge3/etc/profile.d/conda.sh` |
| Activar entorno pyhpc | `conda activate pyhpc` |
| Desactivar entorno | `conda deactivate` |
| Ver entornos disponibles | `conda info --envs` |
| Crear nuevo entorno | `conda create -n nombre-entorno python=3.11` |

## 🛠️ Solución de problemas en mi PC

### Si dice "conda: command not found"

**Solución:** Siempre hago el Paso 1 primero:
```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
```
Luego cierro y vuelvo a abrir la terminal.

### Si el entorno pyhpc no aparece

**Solución:** Verifico que existe y lo recreo si es necesario:
```bash
conda info --envs  # Verificar que pyhpc está listado
conda activate pyhpc  # Intentar de nuevo
```

### Si los paquetes no cargan

**Solución:** Recreate el entorno (hasta ahora me ha pasado una vez):
```bash
conda env remove -n pyhpc --all
conda env create -f /home/izpz/Projects/python-for-hpc-clase-nuevo/python-for-hpc-clase/environment.yml
conda activate pyhpc
```

---

## 📋 Resumen rápido (copy-paste listo para usar)

Para activar mi entorno en cualquier momento, ejecuto estos 3 comandados seguidos:

```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
conda activate pyhpc
python -c "import numpy, scipy, numba, dask, matplotlib; print('Entorno OK')"
```

---

## 📁 Archivo en mi repositorio

Este documento fue creado y guardado en:
```
/home/izpz/Projects/python-for-hpc-clase-nuevo/python-for-hpc-clase/ACTIVACION-PERSONAL.md
```

Puedo verlo y editarlo con:
```bash
code ACTIVACION-PERSONAL.md  # o cualquier editor de texto
```