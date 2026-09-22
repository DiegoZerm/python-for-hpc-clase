# Cómo Activar el Entorno Conda pyhpc

Esta documentación explica cómo activar el entorno `pyhpc` creado para el curso de Python para HPC.

## 📋 Resumen rápido

```bash
# 1. Source el profile de conda
source /ruta/a/miniforge3/etc/profile.d/conda.sh

# 2. Activar el entorno
conda activate pyhpc

# 3. Verificar que funciona
python -c "import numpy, scipy, numba, dask, matplotlib; print('Entorno OK')"
```

---

## 📦 Paso 1: Instalar Miniforge (si no lo tienes)

Si aún no tienes Miniforge instalado, ejecuta:

```bash
# Descargar Miniforge
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"

# Instalar (aceptar defaults presionando Enter/Yes)
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
```

**Verificar instalación:**
```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
conda --version
# Debería mostrar: conda 26.7.2
```

---

## 🔧 Paso 2: Source el profile de Conda

Cada vez que abras una terminal nueva, ejecuta:

```bash
source /ruta/donde/instalaste/miniforge3/etc/profile.d/conda.sh
```

**Ejemplo en este sistema:**
```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
```

*Esto configura el comando `conda` en tu PATH.*

---

## 🌿 Paso 3: Activar el entorno pyhpc

Después de hacer el `source` del paso 2, activa el entorno:

```bash
conda activate pyhpc
```

**Verificación:**
Tu terminal debería mostrar `(pyhpc)` al inicio, como:

```
(pyhpc) izpz@linux:~/Projects$
```

---

## ✅ Paso 4: Verificar que todo funciona

Con el entorno activado, confirma que los paquetes están instalados:

```bash
python -c "import numpy, scipy, numba, dask, matplotlib; print('Entorno OK')"
```

**Resultado esperado:**
```
Entorno OK
```

---

## 🔢 Paso 5: Verificar los cores del CPU

El notebook 01--Introduccion.ipynb solicita verificar:

```bash
python -c "import os; print('Número de cores:', os.cpu_count())"
```

**Resultado esperado (en este sistema):**
```
Número de cores: 8
```

---

## 📓 Paso 6: Iniciar Jupyter Lab (opcional)

Para abrir el notebook del curso:

```bash
jupyter lab
```

Se abrirá en tu navegador en `http://localhost:8888/lab`.

---

## 📁 Archivos relacionados en este repositorio

- `environment.yml` - Especifica los paquetes del entorno
- `01--Introduccion.ipynb` - El notebook principal
- `CONDA-ACTIVATION.md` - Este documento

---

## 🛠️ Solución de problemas comunes

### "conda: command not found"

**Solución:** Asegúrate de haber ejecutado el Paso 2:
```bash
source /home/izpz/miniforge3/etc/profile.d/conda.sh
```

Luego cierra y vuelve a abrir la terminal, o ejecuta de nuevo este comando.

### "environment.yml file not found"

**Solución:** Verifica que estás en el directorio correcto:
```bash
cd /ruta/al/repositorio/python-for-hpc-clase
```

### El entorno no tiene los paquetes esperados

**Solución:** Recreate el entorno:
```bash
conda env remove -n pyhpc --all
conda env create -f environment.yml
conda activate pyhpc
```

### Problemas con Jupyter Lab

**Solución:** Si Jupyter no inicia, intenta reinstalar:
```bash
conda install -c conda-forge jupyterlab
```