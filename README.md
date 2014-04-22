# Base 16 for IPython Notebook

An ipython extension to load custom matplotlibrcs to accompany Nikhil S's [style sheets][0] for [IPython Notebook][1], using Chris Kempson's [Base16][2] color scheme generator 

## Screenshots

####Ocean dark


####Solarized light


## Installation

To use these styles, you'll install this extension in the extensions folder of your ipython
profile. If you don't have a custom profile, run:

`ipython profile create <profile-name>`

To locate the directory of your profile, do:

`ipython locate profile <profile-name>`

You can copy this directory into the `extensions` directory of your profile. Once loaded, this extension can be loaded as any other ipython extension

Using the `%load_ext` magic:
``In [1]: %load_ext base16-mplrc/eighties.dark``

or my modifying your `ipython_notebook_config.py` in your profile directory
``c.InteractiveShellApp.extensions = [
    'base16-mplrc/eighties.dark'
    ]``

## Custom fonts
You can set the default fonts by modifying the base file in base-16, eg:

```
{
  font-family: 'Inconsolata', monospace !important;
  font-size: 16px;
}
```

## Credits

* Uses Base16 builder by [Chris Kempson][3]. 
* Based off of base16-ipython-notebook by [Nikhil S][0]. 

[0]: https://github.com/nsonnad/base16-ipython-notebook
[1]: http://ipython.org/notebook.html
[2]: https://github.com/chriskempson/base16
[3]: https://github.com/chriskempson
[4]: https://github.com/idleberg/base16-codemirror
[5]: https://github.com/idleberg

