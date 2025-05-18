from textual.screen import ModalScreen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.message import Message


class ContextSelector(ModalScreen):

    class ContextSelected(Message):
        def __init__(self, sender, context_name: str):
            self.context_name = context_name
            super().__init__(sender)

    def __init__(self, contexts: list[str]):
        super().__init__()
        self.contexts = contexts

    def compose(self):
        yield Static("🌐 Select a Kubernetes context:", classes="dialog-title")
        yield OptionList(*(Option(name) for name in self.contexts))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss()
        self.post_message(self.ContextSelected(self, event.option_id))  # ✅ emit message to app