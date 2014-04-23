'''
This will theme the inline backend of maptlotlib using base16 fonts

It integrates with Nikhil Sonnad's base16-ipython-notebook themes,
available here:  https://github.com/nsonnad/base16-ipython-notebook

Invoke this via inline magic

`%base16_mplrc`

will try to determine the base16 theme if you have used one of Nikhil's

otherwisr

`%base16_mplrc <shade> <theme>`

will load the theme <theme> in <shade>. e.g.,

`%base16_mplrc dark solarized`
'''
#-------------------------------------------------------
# This extension defines a magic that will configure
# InlineBackend.rc to match the active base16 custom.css
# file, if present
#-------------------------------------------------------

#-------------------------------------------------------
# imports
#-------------------------------------------------------

#stdlib
import os
import re
import json
import glob

#ipython
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.utils.warn import error
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)

@magics_class
class MPLRCMagics(Magics):
    def __init__(self,shell):
        super(MPLRCMagics,self).__init__(shell)

    @line_magic
    @magic_arguments()
    @argument('shade', nargs='?', default = None,help='shade of theme, light or dark')
    @argument('theme', nargs='?', default=None, help='base16 theme')
    def base16_mplrc(self,args):
        #parse the magick arguments
        args = parse_argstring(self.base16_mplrc,args)
        shade = args.shade
        theme = args.theme

        #detect the base16 ipython notebook theme, setup the matplotlib rc
        css_theme = None
        css_shade = None
        custom_css_fname = self.shell.profile_dir.location+'/static/custom/custom.css'
        if os.path.exists(custom_css_fname):
            with open(custom_css_fname) as css_file:
                for line in css_file:
                    if(re.match('^\s*Name: ',line)):
                        css_theme = line.split()[2].lower()
                        css_shade = line.split()[-1].lower()

        #fall back on sensible defaults
        if theme is None:
            theme = css_theme
        if shade is None:
            shade = css_shade
        if theme is None:
            print('''
                     Could not detect base-16 ipython notebook theme. Download base16 theme notebook theme
                     from https://github.com/nsonnad/base16-ipython-notebook . Using \'default\' theme.''')
            theme='default'

        if shade is None:
            print('''
                     Could not detect base-16 ipython notebook theme shade. Download base16 theme notebook themes
                     from https://github.com/nsonnad/base16-ipython-notebook . Using \'default\' theme.''')
            shade = 'light'

        avail_themes = [os.path.split(f)[-1].split('.')[0] for f in glob.glob(self.shell.ipython_dir+'/extensions/base16-mplrc-themes/*.json')]
        #validate input
        if shade not in ['dark','light']:
            print("shade must be either dark or light, defaulting to light")
            shade = 'light'
        if theme not in avail_themes:
            print("theme must be present in base16-mplrc-themes dir, defaulting to 'default'")
            print("Available themes:")
            for t in avail_themes:
                print("\t{}".format(t))
            theme = 'default'

        print("Setting plotting theme to {}-{}".format(theme,shade))
        theme_colors = json.load(open(self.shell.ipython_dir+'/extensions/base16-mplrc-themes/'+theme+'.json'))
        #snag the matplotlibrc configuration from the ipython config
        from IPython.kernel.zmq.pylab.backend_inline import InlineBackend
        cfg = InlineBackend.instance(parent=self.shell)
        cfg.shell=self.shell
        if cfg not in self.shell.configurables:
            self.shell.configurables.append(cfg)
        if shade=="dark":
             cfg.rc = {'figure.facecolor':theme_colors['base00'],
                        'savefig.facecolor':theme_colors['base00'],
                        'text.color':theme_colors['base07'],
                        'axes.color_cycle':[theme_colors['base{:02X}'.format(i)] for i in range(15,8,-1)],
                        'axes.facecolor': theme_colors['base01'],
                        'axes.edgecolor': theme_colors['base01'],
                        'axes.labelcolor': theme_colors['base07'],
                        'lines.color': theme_colors['base09'],
                        'lines.markeredgewidth': 0,
                        'patch.facecolor': theme_colors['base09'],
                        'patch.edgecolor': theme_colors['base02'],
                        'xtick.color': theme_colors['base07'],
                        'ytick.color': theme_colors['base07'],
                        'grid.color': theme_colors['base02']}
        elif shade=="light":
            cfg.rc = {'figure.facecolor':theme_colors['base07'],
                      'savefig.facecolor':theme_colors['base07'],
                      'text.color':theme_colors['base00'],
                      'axes.color_cycle':[theme_colors['base{:02X}'.format(i)] for i in range(15,8,-1)],
                      'axes.facecolor': theme_colors['base07'],
                      'axes.edgecolor': theme_colors['base00'],
                      'axes.labelcolor': theme_colors['base00'],
                      'lines.color': theme_colors['base0D'],
                      'lines.markeredgewidth': 0,
                      'patch.facecolor': theme_colors['base0D'],
                      'patch.edgecolor': theme_colors['base02'],
                      'xtick.color': theme_colors['base00'],
                      'ytick.color': theme_colors['base00'],
                      'grid.color': theme_colors['base06']}
        #If pyplot is already using the InlineBackend, this will force an update to the rcParams
        from matplotlib import pyplot
        if pyplot.rcParams['backend'] == 'module://IPython.kernel.zmq.pylab.backend_inline':
            pyplot.rcParams.update(cfg.rc)

def load_ipython_extension(ipython):
    ipython.register_magics(MPLRCMagics)
