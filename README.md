# Oh My Py

As it turns out, [ipython](http://ipython.org/) is actually really good at being a command shell, though it needs a little bit of tuning out of the box to really be usable as a day-to-day replacement for `fish`, `zsh`, et al.

`ohmypy` aims to address the tuning part of that by overriding some of IPython's default behavior and adding more shell-like functionality.

Right now it's pretty small, not extensively tested, and based more on my own preferences than anything else. In its current work-in-progress state I'd consider it a decent jumping-off point to learn how to build the same kind of thing yourself, but it's not exactly production ready.


## Install

    $ git clone https://github.com/ianpreston/ohmypy.git
    $ virtualenv /path/to/ohmypy/venv
    $ /path/to/ohmypy/venv/bin/pip install ipython pexpect
    $ /path/to/ohmypy/venv/bin/ipython profile create sh
    $ ln -s /path/to/ohmypy/extension/ ~/.ipython/extensions/ohmypy
    $ ln -s /path/to/ohmypy/config.py ~/.ipython/profile_sh/ipython_config.py


## License

The MIT License (MIT)

Copyright (C) 2014 Ian Preston

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
