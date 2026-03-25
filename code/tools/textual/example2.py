"""

A Textual application with some basic functionality.

"""

import sys
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Log, Label, Footer, Header, Markdown, Digits


class Buttons(HorizontalGroup):
    
    def compose(self) -> ComposeResult:
        yield Button("Increment", id='increment', variant='primary')
        yield Button("Reset", id='reset', variant='primary')



class TimeDisplay(Digits):
    """A widget to display elapsed time."""

    pass


class StopwatchWithLabel(VerticalScroll):

    def __init__(self, label: str):
        super().__init__()
        self.label = label

    def compose(self):
        yield Label(self.label)
        yield Stopwatch()


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        self.query_one(Label).text = 'Hoppa!'
        if event.button.id == "start":
            self.add_class("started")
        elif event.button.id == "stop":
            self.remove_class("started")

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class ExampleApp(App):

    counter = 0

    CSS_PATH = "example1.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("i", "increment", "Increment"),
        ("r", "reset", "Reset"),
        ("x", "reset_styles", "Reset styles")]

    def __init__(self):
        super().__init__()

    def counter_line(self):
        return f'>>> counter: {self.__class__.counter}'

    def on_button_pressed(self, event: Button.Pressed) -> None:
        label = self.query_one(Label)
        label.text = f'>>> <Button id={event.button.id} event={str(event)}>'
        print('button pressed')
        print(label)
        print(label.text)
        if event.button.id == "increment":
            self.action_increment()
        if event.button.id == "reset":
            self.action_reset()

    def on_mount(self):
        pass

    def on_ready(self) -> None:
        return
        log = self.query_one(Log)
        log.write_line("Hello, World!")
 
    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown(
            '## Example2\n'
            'Focussing on buttons and styles and...')
        yield Label("Ole")
        #self.log = Log()
        #yield self.log
        for i in range(4):
            yield StopwatchWithLabel(f'StopWatch {i}')
        yield Buttons()
        yield Footer()


    def action_increment(self):
        self.__class__.counter += 1

    def action_reset(self):
        self.__class__.counter = 0

    def action_reset_styles(self):
        text_area = self.query_one(TextArea)
        # these do not work to reset the style
        text_area.styles.reset()
        CSS_PATH = None


if __name__ == '__main__':

    app = ExampleApp()
    app.run()
