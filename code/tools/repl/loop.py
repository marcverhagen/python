"""

Experimenting with the cmd module to build a simple command loop.

In addition we fold in somewhat fancier formatting made available
by the third-party rich module.

To run this:

$ pip install rich
$ python loop.py (--debug)

Resources for the first iteration of this code:

- https://docs.python.org/3/library/cmd.html
- https://www.alcarney.me/blog/2019/til-python-cmd/

"""

import sys
from cmd import Cmd
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()

DEBUG = False


def debug(*texts: list[str]):
    if DEBUG:
        for text in texts:
            print('DEBUG', text)


def get_table():
    """A random table that can be displayed nicely."""
    table = Table(title="Star Wars Movies")
    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")
    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. VIII: The Last Jedi", "$1,332,539,889")
    return table


class Shell(Cmd):

    """The main interactive shell. It maintains a count variable and exposes
    commands that manipulate that variable. Two of the commands are increment 
    and complex_increment

    """

    intro = (
        '\nThis is the shell. Type help or ? for a list of commands.\n'
        '\nHere are some of the most salient commands\n')
    prompt = '(shell) '
    count = 0
    state = None

    def default(self, line):
        """This will apply if no command was recognized."""
        print('>>>', line)
        if line == "q" or line == "EOF":
            return True
        # You can use this to intercept case and send them to some other action,
        # for example here we intercept a number from 0 through 9 and echo it.
        if line in (str(n) for n in range(9)):
            return self.do_echo(line)
        return super().default(line)

    def preloop(self):
        """Just adds printing the most salient commands to the queue."""
        self.cmdqueue.append('help increment')
        self.cmdqueue.append('help complex_increment')
        self.cmdqueue.append('help reset')
        self.cmdqueue.append('help show')
        self.cmdqueue.append('help echo')

    def precmd(self, line):
        """This is done just before the command line is interpreted. Here it just
        debugs the line and hands it over, but it could be used to change the line
        or do some other stuff like logging or some needed set up."""
        debug(f'pre {line}')
        return line

    def postcmd(self, stop, line):
        """This is done after the command line is interpreted, where stop is the
        return value of the command executed. If you set this to True/False you
        can confirm/change whether the loop is terminated."""
        debug(f'post {stop} {line}')
        return stop

    def do_quit(self, arg):
        """All the do_xxx methods have an second argument which will gobble up the
        entire line following the command. If that line has various arguments for
        the underlying code it needs to be parsed here, in cases like this we just 
        ignore it."""
        print('bye bye')
        return True

    def help_quit(self):
        print('quit')
        print('    exit the loop\n')

    def do_echo(self, arg):
        """Prints arg to the output."""
        print(arg)

    # When there is a help_xxx method it will provide the help for do_xxx,
    # if there is not then the docstring of do_xxx is used."""
    def help_echo(self):
        print('echo <arg>')
        print('    Echo the argument.\n')

    def do_show(self, arg):
        """Show the current state of the shell, listing count and state variables
        and throwing in the table."""
        print()
        console.print(Panel('Current settings'))
        console.print(f' state = {Shell.state}')
        console.print(f' count = {Shell.count}')
        console.print(get_table())

    def help_show(self):
        print('show')
        print('    Show the current state of the shell, listing count and state')
        print('    variables and a random table.\n')

    def do_complex_increment(self, arg):
        """Usage: complex_increment

        Calls a subshell to determine a number that will be used for an increment
        in this shell.
        """
        subcount = IncrementShell().cmdloop()
        self.do_increment(subcount)

    def help_complex_increment(self):
        print('complex_increment')
        print('    Calls a subshell to determine a number that will be used for an')
        print('    increment in this shell.\n')

    def do_reset(self):
        self.__class__.count = 0

    def help_reset(self):
        print('reset')
        print('    Reset the count variable to 0.\n')

    def do_increment(self, arg):
        """Increment the count variable with the value provided, increment by
        one if no argument was provided."""
        increment(Shell, arg)

    def help_increment(self):
        print('increment <int>?')
        print('    Increment the counter variable with the value provided,')
        print('    increment by one if no argument was provided.\n')


class IncrementShell(Cmd):

    """This shows how you can run a subshell inside another shell and hand back
    information from the subshell. But note that this is a shell in its own right
    and you can run it indepedently."""

    intro = (
        '\nThis is the increment shell, it helps to settle on an increment value.'
        '\nType help or ? for a list of commands.\n')
    prompt = '(subshell) '
    count = 0

    def preloop(self):
        self.__class__.count = 0
        #print(self.cmdqueue.append('help'))
        #console.print(Panel('Determining increment amount'))

    def cmdloop(self, intro=None):
        """Override cmdloop to return the count value (the default is None). This
        is particularly useful when you use a subshell for some subtask and you
        want to return its handywork to the calling command shell."""
        super().cmdloop(intro)
        return self.__class__.count

    def do_done(self, arg):
        """Usage: done"""
        return True

    def do_increment(self, arg):
        """Usage: increment <int>?

        Increment the counter variable with the value provided, increment by one
        if no argument was provided.
        """
        increment(self.__class__, arg)




def increment(shell_class, arg):
    old_count = shell_class.count
    arg = 1 if not arg else int(arg)
    shell_class.count += arg
    print(f'>>> {shell_class.__name__} increment ::'
          f' {old_count} + {arg} = {shell_class.count}')


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        DEBUG = True
    Shell().cmdloop()
