from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Tree, Label, Log, Footer
from textual.widgets.tree import RemoveRootError


class TreeApp(App):

    CSS_PATH = 'tree.tcss'
    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('c', 'clear', 'Clear log'),
        ('r', 'reset_tree', 'Reset tree'),
        ('d', 'delete_node', 'Delete node')]

    def __init__(self):
        super().__init__()
        self.selected_node = None
        self.init_default_tree()

    def init_default_tree(self, include_root=True):
        if include_root:
            self._tree = Tree("Dune")
        self._tree.root.expand()
        characters = self._tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            with VerticalScroll(classes='wide_column'):
                yield Label('highlighted: ', id='highlighted')
                yield Label('selected:', id='selected')
                yield self._tree
            yield Label('', id='log', classes='narrow_column fullheight')
        yield Footer()

    def on_mount(self):
        pass

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted):
        label = self.query_one('#highlighted')
        label.update(f'highlighted ==> {node_as_string(event.node)}')
        self.log_event('Tree.NodeHighlighted')

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        self.selected_node = event.node
        label = self.query_one('#selected')
        label.update(f'selected    ==> {node_as_string(event.node)}')
        self.log_event('Tree.NodeSelected')
        if event.node.allow_expand:
            added = event.node.add_leaf('dummy')
            self.log_event('TreeNode.add_leaf')

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed):
        self.log_event('Tree.NodeCollapsed')

    def on_tree_node_expanded(self, event: Tree.NodeExpanded):
        self.log_event('Tree.NodeExpanded')

    def action_clear(self):
        self.query_one('#log').update('')
        # See https://textual.textualize.io/api/app/#textual.app.App.notify
        # You can also use severity='warning' or severity='error'
        self.notify('Cleared the log')

    def action_reset_tree(self):
        self.log_event('reset_tree')
        self.query_one(Tree).reset('Dune')
        self.init_default_tree(include_root=False)

    def action_delete_node(self):
        self.log_event('delete_node')
        if self.selected_node is not None:
            try:
                self.selected_node.remove()
                self.selected_node = None
            except RemoveRootError:
                self.log_event('RemoveRootError')

    def log_event(self, event: str):
        log_label = self.query_one('#log')
        log_label.update(f'{log_label.content}{event}\n')


def node_as_string(node):
    return f'<TreeNode id={node.id} label={node.label} parent={node.parent}>'


if __name__ == "__main__":
    app = TreeApp()
    app.run()