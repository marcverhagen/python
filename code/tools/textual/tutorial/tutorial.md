# Textual

[ [home](../readme.md) ]

Notes loosely based on the tutorial at [https://textual.textualize.io/tutorial/](https://textual.textualize.io/tutorial/) which uses files from the [textual](https://textual.textualize.io/tutorial/) repository.


## Installing and running

To install

```bash
pip install textual textual-dev pytest-watch
```

With textual-dev you get [developer tools](https://textual.textualize.io/guide/devtools/) including the console which you can run along the app in separate windows:

```bash
textual console
```

```bash
textual run --dev example1..py
```

This won't give you an automatic restart on file change though. This is where pytest-watch comes in, with that you can start the application as follows:

```bash
ptw --runner "textual run --dev example1.py"
```

Another way to deal with this is to run Textual in server mode (this requires the dev tools):

```bash
textual serve example1.py
```

You can then just point your browser at [http://localhost:8000](http://localhost:8000) and reload after a change.


## General Overview

This has just some of the basics. See [example1.py](example1.py) for the full code, which shows all or most of the concepts in this section. But note that that file has the full *final* code, not every little experiment that was used to write this section, so not all snippets in this code are in the exampe file.

Here is a very basic application:

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class TestApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

if __name__ == '__main__':
    app = TestApp()
    app.run()
```

You create a subclass if textual.app.App and use the run() method and we define the bindings and how the screen is composed. Some magic happens then:

- The bindings are added as tuples to the BINDINGS class variable. The first two elements need to be unique. The second element connects the key with a method, which in the example above is named `action_toggle_dark`. Typically you will define that action in the class but in this case we used one of the builtin actions. Note that in the tutorial there is actually a definition of this action in the class. See [https://textual.textualize.io/guide/actions/](https://textual.textualize.io/guide/actions/) for more on actions. When you start you application the bindings will be loaded and displayed on the footer.

- The `compose` method defines what widgets are part of your screen, in this case two standard widgets: (1) Header contains the name of the application and (2) Footer contains the bindings an da command palette. Without a Footer the bindings will not display but they will still work, for example, pressing 'd' will still toggle dark mode. Without a compose method you just get an empty screen.

Let's start fiddling.


### More on bindings

Adding a couple more bindings and one action:

```python
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("e", "toggle_darker", "Toggle darker mode"),
        ("s", "something", "Do something")]

    def action_something(self):
        print('Doing something')
```

The first one is again to a builtin action so on pressing 'q' the application will quit. For the third binding there is no method named `action_toggle_darker` and it will do nothing (it will write a note to the console in dev mode). For the fourth we do have an action which will just print 'Doing something' to the console.

If you do not add a Footer then you won't see your binding, but the defined key strokes will still be available. By opening the control palette and selecting Keys you get a list of all keys. Open the palette again and select Keys again will hide the key bindings. When there is no Footer you won't see the palette command, but you can also click the circle on the left of the Header or use ^p to open it.


### Adding a text area and a button

Let's add a read-only text area and a button that updates the text in that area.

```python
    def compose(self) -> ComposeResult:
        self.text_area = TextArea(read_only=True, disabled=True)
        yield Header()
        yield self.text_area
        yield Button("Increment", id='increment', variant='primary')
        yield Footer()
```

We store the TextArea in an instance variable so we can access it later. We disable the TextArea which means that is will never be active and grab focus (with some sub-optimal side effects like hiding the binding buttons), you can still programmatically set the text though. A Button can have an action associated with it, but in this case we use the special method `on_button_pressed` which is added to the TextApp class:

```python
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "increment":
            self.__class__.counter += 1
            self.text_area.text = f'Actions: {self.__class__.counter}'
```

If you don't want to store the TextArea in a variable you can simply retrieve it using `query_one()`:

```python
    def compose(self) -> ComposeResult:
        yield TextArea(read_only=True, disabled=True)
        yield Button("Increment", id='increment', variant='primary')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "increment":
            self.__class__.counter += 1
            self.query_one(TextArea).text = f'Actions: {self.__class__.counter}'
```

This will of course require the counter class variable.

You can group the buttons in a container:

```python
class Buttons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Reset", id='reset', variant='primary')
        yield Button("Increment", id='increment', variant='primary')

class TextApp(App):
   def compose(self) -> ComposeResult:
        yield TextArea(read_only=True, disabled=True)
        yield Buttons()
```

### Adding a DataTable

Now we add a table to store the count. There are three parts to this. First you need the data, in the example we just added an instance method:

```python
    def rows(self):
        return [('property', 'value'), ('counter', self.__class__.counter)]
```

Then we add it to the compose method:

```python
    def compose(self) -> ComposeResult:
        ...
        yield Label('And below is the counter in a DataTable.')
        yield DataTable()
        ...
```

Finally, you add the row data to the table

```python
    def on_mount(self):
        rows = self.rows()
        table = self.query_one(DataTable)
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])
```

Here we initialize the table by defining the columns and then add the rows. When adding more data later you would not use `add_columns` again. The `on_mount` method is an event handler that can be defined on an application or a widget. On a widget it is called when the widget is first added to the application, on the application it is called after it enters application mode. 

From [https://textual.textualize.io/guide/app/](https://textual.textualize.io/guide/app/):

> Textual has an event system you can use to respond to key presses, mouse actions, and internal state changes. Event handlers are methods prefixed with on_ followed by the name of the event.
> 
> One such event is the mount event which is sent to an application after it enters application mode. You can respond to this event by defining a method called on_mount.


### Styling

You can add styles directly to the classes, for example:

```python
class Buttons(HorizontalGroup):
    def __init__(self):
        super().__init__()
        self.styles.background = "darkred"
        self.styles.padding = 1
```

But the better way is to use the CSS support that Textual provides. Here is a Textual stylesheet:

```css
Button {
	margin: 2;
}
```

And then you use a special variable to register the stylesheet:

```python
class TestApp(App):
    CSS_PATH = "example1.tcss"
```

You can use variables inside a style sheet:

```css
$border: solid darkgreen;

Label {
	border: $border;
}
```


### More

Doing this makes the bindings in the footer go away:

```python
    def compose(self) -> ComposeResult:
        yield Header()
        yield TextArea()
        yield Footer()
```

This is because the text area grabs focus and in many UI frameworks the bindings disappear when that happens, which makes sense because at that point typing a 'd' should add a 'd' to the text area and not toggle the dark mode. 

Recall how the compose method was setting an instance variable to keep track of the TextArea. It is tempting to do that in an init method, which is great, but do not forget to call init on super.

```python
    def __init__(self):
        super().__init__()
        self.text = TextArea(read_only=True)
```

Be aware of this error:

```
AttributeError: property 'tree' of 'TreeApp' object has no setter
(textual) [13:22:58] textual > textual run --dev widgets/tree.py
Traceback (most recent call last):
  File "/Users/marc/Dropbox/textual/widgets/tree.py", line 67, in <module>
    app = TreeApp()
  File "/Users/marc/Dropbox/textual/widgets/tree.py", line 14, in __init__
    self.tree = Tree("Dune")
    ^^^^^^^^^
AttributeError: property 'tree' of 'TreeApp' object has no setter
```

This happens when you define a variable that is already used.

The tcss extension stands for Textual CSS.


