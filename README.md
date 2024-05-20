# NanoVer Documentation

Sphinx documentation for NanoVer. 

## Getting Started

Clone the repo, open a terminal, and install the dependencies: 

```
python -m pip install -r requirements.txt
```

(OPTIONAL) In order to also build the docstring documentation, you also need to 
install `nanover-server` and `nanover-lammps`:

```
conda install -c irl -c conda-forge nanover-server
conda install -c irl -c conda-forge nanover-lammps
```

Make sure the submodules are initialised: 

```
git submodule update --init --recursive
```

To build the docs, on Linux/ Mac OS X:

```
make html
```

On Windows:

```
./make.bat html
```

## Posting to readthedocs 

The repository automatically tracks updates to the nanover-protocol repository, 
and a webhook exists on readthedocs to build the documentation. 

