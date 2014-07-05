c = get_config()

c.TerminalIPythonApp.display_banner = False
c.InteractiveShell.automagic = False
c.InteractiveShellApp.extensions = [
    'ohmypy',
]

c.PromptManager.in_template  = r'{color.LightBlue}\u@\h {color.Green}\w {color.White}~> '
c.PromptManager.in2_template = r'{color.White}\D ~>'
c.PromptManager.out_template = r'=> '
