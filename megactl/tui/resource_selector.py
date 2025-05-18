from textual.screen import ModalScreen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option


class ResourceSelector(ModalScreen[str]):
    def __init__(self, kind: str, resources: list[str]):
        super().__init__()
        self.kind = kind
        self.resources = resources

    def compose(self):
        yield Static(f"🔽 Select a {self.kind}", classes="dialog-title")
        options = [Option(name, id=name) for name in self.resources]
        yield OptionList(*options)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(event.option_id)
