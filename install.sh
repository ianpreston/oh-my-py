#!/bin/sh
if [ ! -d "extension" ]; then
    echo "Script must be run from within oh-my-py install directory"
    exit 1
fi

ipython profile create sh
rm $HOME/.ipython/profile_sh/ipython_config.py || true
rm $HOME/.ipython/extensions/ohmypy || true
ln -s `pwd`/extension $HOME/.ipython/extensions/ohmypy
ln -s `pwd`/config.py $HOME/.ipython/profile_sh/ipython_config.py

echo "Success! Now run IPython like this: $ ipython --profile sh"
echo "See `pwd`/README.md for more information"
