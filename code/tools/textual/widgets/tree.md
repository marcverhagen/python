# Textual - The Tree Widget

[ [home](../readme.md) ]

This shows how to (1) build a Tree, (2) react to highlight and select events, (3) add subnodes to a tree node, (4) access information on tree nodes, and (5) write the state of the tree to other widgets. It also shows an alternative way to build the widget tree.

Useful links:

- [https://textual.textualize.io/widgets/tree/](https://textual.textualize.io/widgets/tree/)
- [https://textual.textualize.io/widgets/tree/#textual.widgets.tree.TreeNode](https://textual.textualize.io/widgets/tree/#textual.widgets.tree.TreeNode)

This is expanding on an example in the first link above, the full code is in [tree.py](tree.py).


### Initialization

We start with a TreeApp that initializes a tree:

```python
class TreeApp(App):

    def __init__(self):
        super().__init__()
        self._tree = Tree("Dune")
        self._tree.root.expand()
        characters = self._tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
```

The value of `root` is an instrance of TreeNode, which supports methods `add()` and `add_leaf(). The former is to add a subtree, which in this case will be expanded on the screen, the latter is to add a leaf node, which is also an instance of TreeNode.

Another thing to note here is that we use `_tree` to store the Tree widget and not `tree`, this is because the latter is already occupied by an object of type `rich.tree.Tree`. For some reason that attribute was not listed in the reference page for Tree.

> Maybe other Widgets also have an attribute for rich classes since I had trouble using the log attribute on a Log instance. Check this.
> 
> Wait, that cannot be the case since we are working with an instance of textual.app.App.


### Composing

Adding a compose method:

```python
    def compose(self) -> ComposeResult:
        yield Label('highlighted: ', id='highlighted')
        yield Label('selected:', id='selected')
        yield Label('', id='log')
        yield self._tree
        yield Footer()
```

We have three labels, a tree and a footer. The labels all have identifiers so we can change them easily later. The code above is not in the example file anymore and was replaced with 

```python
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            with VerticalScroll(classes='wide_column'):
                yield Label('highlighted: ', id='highlighted')
                yield Label('selected:', id='selected')
                yield self._tree
            yield Label('', id='log', classes='narrow_column fullheight')
        yield Footer()
```

Here we use context managers and make the hierarchy explicit in the one compose method. When you do this you have to be careful with your styles, in particular do not set widths to 100%. In the example we use classes to set fractional widths and a full height for the log on the right.


### Highlighting

Here is a method to intercept the highlight event, along with a utility method (and `node_as_string` is another utility that prints a TreeNode):

```python
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted):
        label = self.query_one('#highlighted')
        label.update(f'highlighted ==> {node_as_string(event.node)}')
        self.log_event('Tree.NodeHighlighted')

    def log_event(self, event: str):
        log_label = self.query_one('#log')
        log_label.update(f'{log_label.content}{event}\n')
```

There are four classes corresponding to events sent after changes in the tree, corresponding with four event handler methods:

| class | handler |
| ----- | ------- |
| Tree.NodeCollapsed   | `on_tree_node_collapsed`   |
| Tree.NodeExpanded    | `on_tree_node_expanded`    |
| Tree.NodeHighlighted | `on_tree_node_highlighted` |
| Tree.NodeSelected    | `on_tree_node_selected`    |

With the above code, when a node is highlighted (and when starting the root node will be highlighted, but not selected) we do a couple of things:

- get the node that was highlighted from the event
- find the appropriate label to report this to with `query_one`.
- update the label
- log the event, which includes finding the log and updating it

The helper method `node_as_string` illustrates how to access information on nodes:

```python
def node_as_string(node):
    return f'<TreeNode id={node.id} label={node.label} parent={node.parent}>'
```

We access the id, label and parent attributes, the first and third of which are created automatically when adding nodes. See the [TreeNode](https://textual.textualize.io/widgets/tree/#textual.widgets.tree.TreeNode) section of the Tree reference for other methods available on the node.


### Selecting and adding a subnode

Here is the slightly more useful event handler that deals with selected nodes:

```python
    def on_tree_node_selected(self, event: Tree.NodeSelected):
        label = self.query_one('#selected')
        label.update(f'selected    ==> {node_as_string(event.node)}')
        self.log_event('Tree.NodeSelected')
        if event.node.allow_expand:
            added = event.node.add_leaf('dummy')
            self.log_event('TreeNode.add_leaf')
            self.log_event(str(added))
```

This one adds a dummy node as a child on the selected node but only if it allows that (because it is a non-terminal).

On the difference between highlighting and selected:

- After mounting, the root node is highlighted but not selected.
- Navigating with the up and down keys changes the highlighted node but not the selected node.
- Hitting return will select the highlighted node.
- Clicking a highlighted node will select it (double-clicking will select it twice).
- Clicking a non-highlighted node will highlight and select it double-clicking will highlight once and select twice).


### Deleting a node

For this let's first dig up an error class, for the Tree class they live in textual.widgets.tree:

```python
from textual.widgets.tree import RemoveRootError
```

And let's introduce a binding and an action method:

```python
    BINDINGS = [('d', 'delete_node', 'Delete node')]

    def action_delete_node(self):
        self.log_event('DeleteNode')
        if self.selected_node is not None:
            try:
                self.selected_node.remove()
                self.selected_node = None
            except RemoveRootError:
                self.log_event('RemoveRootError')
```

This method assumes there is a `selected_node` attribute that that contains the selected node and which is set in the `on_tree_node_selected` method.


### Resetting the tree

For resetting the Tree you cannot just change the value of the `_tree` attribute (although maybe that works if you can make it a reactive attribute, but currently I know near nothing about that).

What you can do is to refactor the initialization process a bit by including something like this on the TreeApp class:

```python
    def init_default_tree(self, include_root=True):
        if include_root:
            self._tree = Tree("Dune")
        self._tree.root.expand()
        characters = self._tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
```

And the do this in an action:

```python
    def action_reset_tree(self):
        self.query_one(Tree).reset('Dune')
        self.init_default_tree(include_root=False)
```


### More

Some further questions:

- The delete action deletes a node. The problem is that it tries to delete the selected node whereas the user will think it is deleting the highlighted node. Recall we get the selected node form an instance variable that is updated after each select event, we could do the same with the highlight event. But I am wonder whether it is an option to select after you highlight. And of course you could have a dialog in case highlighted and selected are not the same.