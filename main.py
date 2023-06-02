import sys
import time
import yaml

from rich import pretty
from rich.console import Console

from core.cp import format_cp

last_result = None
local_plug_namespace = {}

def get_text_after_input(args):
    if "input" in args:
        index = args.index("input")
        text = " ".join(args[index + 1:])
        return text
    else:
        return None

def get_text_after_plugins(args):
    if "plugins" in args:
        index = args.index("plugins")
        text = args[index + 1]
        return text.split(",")
    else:
        return []

if __name__ == '__main__':
    startTime = time.time()
    console = Console()

    if 'noInspectors' not in sys.argv:
        import inspectors
        inspectors.init()

    if 'noPromptExecutor' not in sys.argv:
        from core import executor

        executor.initPlugins(get_text_after_plugins(sys.argv))

    if 'noPrompt' not in sys.argv:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
        from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
        from prompt_toolkit.completion import NestedCompleter
        from prompt_toolkit.history import FileHistory
        from prompt_toolkit.lexers import PygmentsLexer
        from prompt_toolkit.output import ColorDepth
        from prompt_toolkit.shortcuts import CompleteStyle
        from prompt_toolkit.styles import Style
        from pygments.lexers.python import Python3Lexer

        our_history = FileHistory("./mount/.history")

        # The history needs to be passed to the `PromptSession`. It can't be passed
        # to the `prompt` call because only one history can be used during a
        # session.
        session = PromptSession(history=our_history)

        style = Style.from_dict({
            # User input (default text).
            '': 'white bold',

            # Prompt.
            'name': 'ansicyan bold',
            'pound': '#00aa00 default',
            'user_prompt': 'bold',
            'path': 'yellow underline',
        })

    if 'compact' not in sys.argv:
        from frosch import hook, print_exception
        import pretty_traceback
        import pyfiglet

        hook()

        pretty.install()
        pretty_traceback.install()

        ascii_banner = pyfiglet.figlet_format("Taser://")

        print(ascii_banner)
        console.print(
            "Taser Prism is an open source program designed to\nanalyze the source code of android applications")

        print("")

        with open("data/lib_detect.yml", 'r') as document:
            console.print(
                f"🗃️️   Known libraries for indexing in code: [orange]{len(yaml.safe_load(document).get('libs').keys())}[/]")

        with open("./mount/unicorn.txt", 'r') as document:
            console.print(f"🦄  Libraries synchronized: [orange bold]{len(document.readlines())}[/]")

        console.print(
            "🕔  Runtime is a " + str(round(time.time() - startTime, 2)) + " seconds")

        console.print(
            "Taser also supports the [red bold]Revisoro[/] utilite to analyze code inheritance out of the box ")

        print("")

    if 'telnet' in sys.argv:
        import adapter.telnet

        console.print("🌍 Expansion to the world!!! You use telnet mode. ")

        adapter.telnet.main()

    if 'input' in sys.argv:
        text = get_text_after_input(sys.argv)
        executor.input_execute(text)
        exit(0)

    while True:
        try:
            message = [
                ('class:name', "taser"),
                ('', ':'),
                ('class:path', f"{format_cp()}"),
                ('class:pound', '/> '),
                ('class:user_prompt', ''),
            ]

            if 'noPrompt' not in sys.argv:
                text = session.prompt(
                    message,

                    lexer=PygmentsLexer(Python3Lexer),
                    completer=NestedCompleter.from_nested_dict(executor.completer_dict),
                    style=style,
                    clipboard=PyperclipClipboard(),
                    complete_style=CompleteStyle.COLUMN,
                    enable_history_search=True,
                    refresh_interval=0.5,
                    auto_suggest=AutoSuggestFromHistory(),
                    color_depth=ColorDepth.TRUE_COLOR
                )

            else:
                exit(0)

            try:
                if text and 'noPromptExecutor' not in sys.argv:
                    exclude = executor.input_execute(text)

                    if not isinstance(exclude, list):
                        if 'noPrompt' not in sys.argv:
                            console.print(
                                exclude,
                                highlight=True,
                                no_wrap=False,
                                markup=True
                            )
                        else:
                            print(exclude)

                    else:
                        for line in exclude:
                            if 'noPrompt' not in sys.argv:
                                console.print(
                                    line,
                                    highlight=True,
                                    no_wrap=False,
                                    markup=True
                                )
                            else:
                                print(line)

            except Exception as error:
                if 'compact' not in sys.argv:
                    print_exception(error)
                else:
                    print(error)

        except KeyboardInterrupt:
            exit(0)
