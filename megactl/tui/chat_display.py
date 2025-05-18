from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from textual.scroll_view import ScrollView


class ChatDisplay(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []

    def add_user_message(self, message: str):
        self.lines.append(("user", f"🧑 {message}"))
        self.refresh()
        self.call_after_refresh(self.scroll_end)

    def add_bot_message(self, message: str):
        self.lines.append(("bot", f"🤖 {message}"))
        self.refresh()
        self.call_after_refresh(self.scroll_end)

    def add_output(self, message: str, success: bool = True):
        emoji = "✅" if success else "❌"
        style = "green" if success else "red"
        self.lines.append(("output", f"[{style}]{emoji} {message}[/]"))
        self.refresh()
        self.call_after_refresh(self.scroll_end)

    def clear_display(self):
        self.lines = []
        self.refresh()

    def render(self):
        text = Text()
        for role, msg in self.lines[-100:]:
            if role == "output" and msg.strip().startswith("```"):
                text.append(Markdown(msg))
            else:
                text.append(Text.from_markup(msg))
            text.append("\n")
        return Panel(text, title="Session", border_style="default")
