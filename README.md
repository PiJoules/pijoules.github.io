# New Personal Website
The `build` branch contains the source that uses pelican.
The `master` branch contains the generated html.

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

#### [Pelican Github Projects](https://github.com/kura/pelican-githubprojects)
This project also depends on Pelican Github Projects, but there is a change
that I made to the source that I am waiting for the owner to add from my
pull request. Untill that is made, I use my own forked copy with the changes
I implemented.

To use this version instead of the original:
```sh
(personal-website) $ git clone https://github.com/PiJoules/pelican-githubprojects
(personal-website) $ cd pelican-githubprojects
(personal-website) $ python setup.py bdist_wheel
(personal-website) $ python wheel install dist/pelican_vimeo-0.1.0-py2.py3-none-any.whl
```

### Starting Development server
```sh
(personal-website) $ make devserver
```

### Deploying to github
```sh
(personal-website) $ make github
```
