# oh-my-py

[IPython](http://ipython.org/) isn't only an excellent Python REPL -- it can be a formidable general-purpose command shell if configured properly, easily capable of being a replacement for `zsh`, `fish`, et al.

`oh-my-py` is a proof-of-concept command shell *thing* for IPython. It's somewhere between a collection of utilities, and a fully-featured command shell. Essentially, it's a brain dump of various IPython-as-a-command-shell ideas.


## Example

    > fn = 'test.txt'
    > with open(fn, 'w') as f:
          f.write('Hello world!')
    > x = `cat test.txt`
    > print x
    Hello world!
    > vim {fn}
    > x = !cat {fn}
    > print x
    Hello edited file!


## Install

Clone the git repository and run the install script:

    $ git clone https://github.com/ianpreston/oh-my-py.git && cd oh-my-py
    $ ./install.sh

You can run it from your existing shell to give it a try:

    $ /usr/bin/login -f -l YOUR_USERNAME /usr/local/bin/ipython --profile sh

Or, more simply:

    $ ipython --profile sh


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
