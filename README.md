# Narupa Documentation

Sphinx documentation for Narupa. 

## Getting Started

Clone the repo, open a terminal, and install the dependencies: 

```
python -m pip install -r requirements.txt
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

The repository automatically tracks updates to the narupa-protocol repository, 
and a webhook exists on readthedocs to build the documentation. 

## Updating the environment

ReadTheDocs uses a `environment.yml` file to set the conda environment. To
create this file:

```
conda create -n doc -c omnia -c conda-forge python MDAnalysis openmm
conda activate doc
conda env export > environment.yml
```