from textual.containers import Vertical, Horizontal
from textual.widgets import Static

from megactl.tui.chat_display import ChatDisplay
from megactl.tui.prompt_input import PromptInput


def build_main_layout(input_box: PromptInput) -> Vertical:
    """Builds the main layout with chat and input row."""
    return Vertical(
        ChatDisplay(id="chat", classes="chat"),
        Horizontal(
            input_box,
            id="input-row"
        ),
        id="main-layout"
    )
