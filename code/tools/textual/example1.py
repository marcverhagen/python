"""

A Textual application with some basic functionality.

"""

import sys
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, Label, Footer, Header
from textual.widgets import TextArea, Markdown, DataTable

text_area_splash = (
    'This is a TextArea. It is created as a read-only TextArea that does not '
    'highlight the cursor line because that would be distracting. You could '
    'also disable it with disabled=True which would prevent it from taking '
    'focus but then the outline will be dimmed.\n\n'
    'We use this TextArea to print the counter, which is probably better done '
    'with a Label or a DataTable.'
    )

class Buttons(HorizontalGroup):
    
    def compose(self) -> ComposeResult:
        yield Button("Increment", id='increment', variant='primary')
        yield Button("Reset", id='reset', variant='primary')


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
        self.text_area = TextArea(
            read_only=True, highlight_cursor_line=False)
        self.text_area.text = text_area_splash + '\n\n' + self.counter_line()

    def rows(self):
        return [('property', 'value'), ('counter', self.__class__.counter)]

    def refresh_text_area(self):
        text = f'{text_area_splash}\n\n>>> counter: {self.__class__.counter}'
        self.query_one(TextArea).text = text
        # You can also access the text area from the instance variable
        # self.text_area.text = text

    def counter_line(self):
        return f'>>> counter: {self.__class__.counter}'

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "increment":
            self.action_increment()
        if event.button.id == "reset":
            self.action_reset()

    def on_mount(self):
        self.populate_table()

    def clear_table(self):
        self.query_one(DataTable).clear(columns=True)

    def populate_table(self):
        rows = self.rows()
        table = self.query_one(DataTable)
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown(
            '## Simple application with minimal functionality\n'
            'We are playing around with widgets, styles and actions.\n'
            'This is a markdown widget.')
        yield Label(
            'This is a Label widget, which can have multiple lines.\n\n'
            'Here we take the opportunity to say that there is a stylesheet in '
            'example1.tccs, which makes this all look nicer than the defaults.')
        yield self.text_area
        yield Label('And below is the counter in a DataTable.')
        yield DataTable()
        yield Label(
            'The buttons below are associated with actions via the on_button_pressed '
            'method. The key bindings in the footer are associated with action methods.')
        yield Buttons()
        yield Footer()


    def action_increment(self):
        self.__class__.counter += 1
        self.refresh_text_area()
        self.clear_table()
        self.populate_table()

    def action_reset(self):
        self.__class__.counter = 0
        self.refresh_text_area()
        self.clear_table()
        self.populate_table()

    def action_reset_styles(self):
        text_area = self.query_one(TextArea)
        # these do not work to reset the style
        text_area.styles.reset()
        CSS_PATH = None


if __name__ == '__main__':

    app = ExampleApp()
    app.run()
