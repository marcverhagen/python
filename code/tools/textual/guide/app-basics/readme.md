# Textual - App Basics Guide

[ [home](../../readme.md) ]

From [https://textual.textualize.io/guide/app/](https://textual.textualize.io/guide/app/).


### Running inline

You can run an App with the inline=True setting which will run the App while the the command line is still visible above it. For some Apps you may need to add a style, see [inline.py]((inline.py). Not sure when this is needed, maybe for those cases where the App takes the whole screen).


### Events

Event handlers are methods prefixed with on_ followed by the name of the event. 

For example there is the mount event, which is sent to an application after it enters application mode, and the key event, both used in these methods on the App (see [event01.py](event01.py) for the full code):

```python
def on_mount(self) -> None:
    self.screen.styles.background = "darkblue"

def on_key(self, event: events.Key) -> None:
    if event.key.isdecimal():
        self.screen.styles.background = self.COLORS[int(event.key)]
```

Note the screen variable on the App instance, here it gives yu access to the styles.


### Widgets

Widgets are self-contained components responsible for generating the output for a portion of the screen. Widgets respond to events in much the same way as the App.

To add widgets to your app implement a `compose()` method which should return an iterable of Widget instances.

Here is one that uses the Welcome widget, which has a Markdown area and a button (from [welcome01.py](welcome01.py)). Note the `exit()` method on the App instance.

```python
class WelcomeApp(App):
    def compose(self) -> ComposeResult:
        yield Welcome()
    def on_button_pressed(self) -> None:
        self.exit()
```

An alternative here is to use the `mount()` method instead of `compose()`, which can add a new widget (from [welcome02.py](welcome02.py)). In this case you start with an empty screen but after each click a new Welcome widget will be added.

```python
class WelcomeApp(App):
    def on_key(self) -> None:
        self.mount(Welcome())
```

#### Awaiting mounts

[https://textual.textualize.io/guide/app/#awaiting-mount](https://textual.textualize.io/guide/app/#awaiting-mount)

When you mount a widget, Textual will mount everything the widget composes. Textual guarantees that the mounting will be complete by the next message handler, but not immediately after the call to mount(). So the following will not work:

```python
class WelcomeApp(App):
    def on_key(self) -> None:
        self.mount(Welcome())
        self.query_one(Button).label = "YES!"
```

Instead use async:

```python
class WelcomeApp(App):
    async def on_key(self) -> None:
        await self.mount(Welcome())
        self.query_one(Button).label = "YES!"
```


### Exiting

[https://textual.textualize.io/guide/app/#exiting](https://textual.textualize.io/guide/app/#exiting)

An app will run until you call App.exit() which will exit application mode and the run method will return. The exit method can also accept an optional positional value to be returned by run().


### Suspending

