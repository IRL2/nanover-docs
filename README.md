# NanoVer Documentation

Sphinx documentation for NanoVer, see the [documentation here](https://irl2.github.io/nanover-docs/#).

## Getting Started

Clone the repo, open a terminal, and install the dependencies: 

```
python -m pip install -r requirements.txt
```

(OPTIONAL) In order to also build the docstring documentation, you also need to 
install `nanover-server`:

```
conda install -c irl -c conda-forge nanover-server
```

To generate docs for a development version of NanoVer, it is necessary to 
install the NanoVer Python Server from source, the instructions for which
can be found [here](https://github.com/IRL2/nanover-server-py/blob/main/README.md#setup-nanover-server-py-for-developers-on-mac-and-linux).

Make sure the submodules are initialised and updated:

```
git submodule update --init --recursive --remote
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

**If you get warnings about failing to import modules when building the docs locally, reclone the repo.**


## Posting to readthedocs 

The repository automatically tracks updates to the nanover-server-py repository, 
and a webhook exists on readthedocs to build the documentation. 

