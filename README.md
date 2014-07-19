# oh-my-py

[IPython](http://ipython.org/) isn't only an excellent Python REPL -- it can be a formidable general-purpose command shell if configured properly, easily capable of being a replacement for `zsh`, `fish`, et al.

The "configured properly" part is where `ohmypy` comes in. It's kind of like `oh-my-zsh` for IPython. It provides a barebones level of integration between `/bin/sh` and regular Python code, and serves as a starting point on top of which to build your own fully-featured command shell.


## Example

    In [1]: vim test.txt
    In [2]: cat test.txt
    hello 
    In [3]: r = `cat test.txt`
    In [4]: print r[::-1]
    olleh
    In [5]: /bin/echo -n {r}
    hello


## Install

First, create an IPython installation and configure it for `ohmypy`

    $ git clone https://github.com/ianpreston/ohmypy.git
    $ virtualenv /path/to/ohmypy/venv
    $ /path/to/ohmypy/venv/bin/pip install ipython pexpect
    $ /path/to/ohmypy/venv/bin/ipython profile create sh
    $ ln -s /path/to/ohmypy/extension/ ~/.ipython/extensions/ohmypy
    $ ln -s /path/to/ohmypy/config.py ~/.ipython/profile_sh/ipython_config.py

Then, update your terminal emulator to run the new IPython profile as a login session. Here's an example:

    /usr/bin/login -f -l YOUR_USERNAME /path/to/ohmypy/venv/bin/ipython --profile sh


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
