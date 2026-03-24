from code import InteractiveConsole

header = "Entering REPL"
footer = "Exiting REPL"

def pp(stuff):
	print(stuff)

state = {'count': 0}

scope_vars = {'pp': pp, 'state': state}

InteractiveConsole(locals=scope_vars).interact(header, footer)
