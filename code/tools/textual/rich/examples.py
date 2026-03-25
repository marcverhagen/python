from rich.console import Console

console = Console()

print(f'{console.size} is_terminal={console.is_terminal}')

console.print([1, 2, 3])
console.print("[blue underline]Looks like a link")
#console.print(locals())
console.print("FOO", style="white on blue")
console.print("FOO", style="black on red")
console.print("Danger, Will Robinson!", style="blink bold red underline on white")

