# NanoVer Documentation

Sphinx documentation for NanoVer. 

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

Or on Windows:

* Using Command Prompt:
```
make.bat html
```
* Using PowerShell:
```
./make.bat html
```


## Posting to readthedocs 

The repository automatically tracks updates to the nanover-protocol repository, 
and a webhook exists on readthedocs to build the documentation. 

