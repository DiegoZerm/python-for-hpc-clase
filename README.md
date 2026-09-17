# Python para HPC

¡Bienvenido/a al curso **Python para HPC** (Computación de Alto Rendimiento)!

Este material es una traducción y adaptación al español, para estudiantes de licenciatura, del curso *Python for HPC* del Max Planck Computing and Data Facility (MPCDF).

## Créditos

Este curso está basado en el material original creado por:

* Sebastian Kehl (2022 - 2025)
* Sebastian Ohlmann (2018 - 2025)
* Klaus Reuter (2018 - 2025)

[Max Planck Computing and Data Facility (MPCDF), Garching](https://mpcdf.mpg.de/)

Con contribuciones previas de Rafael Lago (2020).

Repositorio original (en inglés): https://gitlab.mpcdf.mpg.de/mpcdf/python-for-hpc-exercises

**Adaptación al español y para licenciatura:** Javier Moya

## Sobre este material

* El material original del MPCDF indica que está pensado para los participantes registrados de su curso, y que su redistribución requiere el consentimiento de los autores. Esta adaptación se comparte con fines educativos para un curso de licenciatura, dando el crédito correspondiente a los autores originales.
* Los notebooks de Jupyter discutidos en las clases están siendo traducidos progresivamente y adaptados con explicaciones adicionales pensadas para quienes ven HPC por primera vez.

## Temario

* Introducción
  * Bases de HPC
* Cómputo numérico eficiente
  * NumPy
  * SciPy
  * Entrada/salida basada en HDF5 con H5Py
  * Interfaz con C/C++, Fortran, CUDA y otras librerías
  * Compilación JIT con Numba y JAX
  * Profiling (medición de rendimiento)
* Ingeniería de software con Python
  * Testing
  * Empaquetado
  * Documentación
* Cómputo paralelo
  * Bases de cómputo paralelo
  * Threading en Python, el GIL
  * Multiprocessing
  * Cómputo en GPU con Numba, CuPy, JAX
  * Frameworks de paralelización, Dask
  * MPI, mpi4py
  * Ejecutar programas paralelos en Python con Slurm
* Ejercicios y ejemplos complementarios
  * Repaso de Python
  * NumPy
  * Código simple de advección
  * Código simple de difusión (MPI)
* Material adicional
  * Repaso de Python
  * Cython
  * Visualización (matplotlib, colores)

## Referencias

Este curso está basado en gran parte en la experiencia de trabajo diario de sus autores originales. Además, se usaron las siguientes fuentes:

* *High Performance Python, Practical Performant Programming for Humans*, Micha Gorelick, Ian Ozsvald, O'Reilly Media; segunda edición, 2020. (En particular, partes del ejemplo de difusión se presentan de forma similar a como se discute en este libro.)
* *A Whirlwind Tour of Python*, Jake VanderPlas, O'Reilly Media, 2016.
* Documentación oficial de Python, NumPy, SciPy, Cython, Numba, mpi4py, etc.

Otras fuentes (menores) se referencian directamente en los notebooks.

## Requisitos de software

### Paquetes de Python

Los ejemplos de este curso están basados en Python 3, NumPy, SciPy, Cython, Numba, matplotlib, mpi4py, Dask, y algunos más.

Para instalar todos los paquetes necesarios de forma sencilla, se recomienda descargar e instalar [Miniforge](https://conda-forge.org/miniforge/) — una alternativa gratuita a las distribuciones comerciales de Python — y usar `conda` o `mamba` junto con el archivo de este repositorio correspondiente a tu sistema operativo, para crear un [entorno de software](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) local:

* **Linux:** usa `environment.yml`
* **macOS o Windows:** usa `environment2.yml` (variante multiplataforma; ver el notebook `01--Introduccion.ipynb` para más detalle)

```bash
conda env create --file environment.yml    # Linux
# o
conda env create --file environment2.yml   # macOS / Windows
conda activate pyhpc
```

### Presentación de slides en Jupyter vía RISE

Es posible presentar las celdas del notebook de Jupyter como diapositivas usando la extensión [RISE](http://rise.readthedocs.io/en/latest/index.html). Para entrar al modo de presentación, presiona <Alt+r> dentro de un notebook.
