# Specialized command line tools

In the past I have used homegrown specialized command line tools for tasks like simple annotations where a GUI did not seem needed (and would in fact slow down the whole process). The problem was that when they became a wee less trivial the code would descend  into some convoluted while loop where a lot of tinkering was required to get everything to behave.

There are third-party libraries like [ReplBuilder](https://github.com/Aperocky/replbuilder) and [prompt-toolkit](https://pypi.org/project/prompt-toolkit/), but at the moment I have nothing intelligent to say on them.

Another option is to rely on the [cmd](https://docs.python.org/3/library/cmd.html) module in the standard library. And I did create some tools with that module and the [rich](https://pypi.org/project/rich/) library.

This folder has several examples of command line tools:

- [repl_python.py](repl_python.py)<br/>
   A simple Python REPL yanked from some internet search. All it
   does is evaluation statements and expressions.

- [repl_vars](repl_vars.py)<br/>
  Another simple Python REPL that adds a couple of locally defined 
  variables and functions to the REPL's namespace. Based on 
  the InteractiveConsole class in the code module from the 
  standard library.

- [repl_turtle.py](repl_turtle.py)<br/>
  The example from the Python [cmd](https://docs.python.org/3/
  library/cmd.html) library.

- [loop.py](loop.py)<br/>
  A more involved annotated example using the cmd module and the 
  rich library, it is cobbled together from various sources 
  including the cmd documentation, a
  [blog post](https://www.alcarney.me/blog/2019/til-python-cmd/)
  by Alex Carney and some other targeted searches. This one also 
  allows non-Python syntax in the commands and is overall a bit
  more powerfull, one thing you can do for example is to fire off
  a sub shell to deal with some subtask and then feed the result 
  back into the main shell.


