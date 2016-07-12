# New Personal Website
The `build` branch contains the source that uses pelican.
The `master` branch contains the generated html and is what is displayed on the
github.io page.
When developing, be sure to clone, checkout, and work on the `build` branch.

## Cloning
This module uncludes submodules, so be sure to add the `--recursive` arg to
clone the submodules also.

You will also be cloning the build branch, so be sure to add the `-b build` args.

Altogether, to get a complete copy of the code for development:
```sh
$ git clone --recursive -b build https://github.com/PiJoules/pijoules.github.io.git
```

## Usage

### Virtualenv
Create a new virtual env to install everything in.

Using `virtualenv`:
```sh
$ virtualenv personal-website
$ source personal-website/bin/activate
```

or

Using [_switch_virtualenv](https://github.com/PiJoules/python-dev-scripts#_switch_virtualenv):
```sh
$ _switch_virtualenv personal-website
```

### Install all dependencies

#### requirements.txt
```sh
(personal-website) $ pip install -r requirements.txt
```

### Starting Development server
```sh
(personal-website) $ make devserver
```

### Deploying to github
```sh
(personal-website) $ make github
```
