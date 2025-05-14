# kubecmd

**UNSTABLE - NOT READY FOR USE IN PRODUCTION**

CLI and Python API providing a simple interface to execute kubernetes jobs.

Inspired by:

- https://github.com/CLIMB-TRE/roz
- https://github.com/telatin/kuberun
- https://github.com/kubernetes-client/python/blob/master/examples/job_crud.py

## Setup

### Build from source

```
$ git clone https://github.com/tombch/kubecmd.git
$ cd kubecmd/
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .
```

## Usage

To run the command `perl -Mbignum=bpi -wle print bpi(2000)` in the `perl:5.34.0` container:

```
$ kubecmd -d perl:5.34.0 -c "perl -Mbignum=bpi -wle print bpi(2000)"
```
