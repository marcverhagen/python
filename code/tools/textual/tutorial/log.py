from textual.app import App, ComposeResult
from textual.widgets import Log


class LogApp(App):
    """An app with a simple log."""

    def compose(self) -> ComposeResult:
        yield Log()

    def on_ready(self) -> None:
        log = self.query_one(Log)
        log.write_line("Hello, World!")


if __name__ == "__main__":
    app = LogApp()
    app.run()
