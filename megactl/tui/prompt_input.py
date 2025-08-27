from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive
from textual.geometry import Offset
from textual.events import Key
from rich.text import Text

from megactl.ai.prompt_completion import get_prompt_suggestion
from megactl.k8s.cluster import resource_cache


class PromptInput(Widget):
    can_focus = True
    show_cursor = True

    prompt = reactive("[default] ")
    value = reactive("")
    cursor = reactive(0)
    suggestion = reactive("")
    suggestion_timer = None

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def render(self) -> Text:
        text = Text(self.prompt)
        text.stylize("bold green", 0, len(self.prompt))

        if not self.value:
            text.append("Type a Kubernetes command...", style="dim")
        else:
            text.append(self.value)
            if self.suggestion and self.has_focus and self.suggestion.startswith(self.value):
                text.append(self.suggestion[len(self.value):], style="dim")

        return text

    def cursor_position(self) -> Offset:
        return Offset(x=len(self.prompt) + self.cursor, y=0)


    def on_key(self, event: Key) -> None:
        key = event.key
        char = event.character
        input_changed = False

        if key == "enter":
            self.post_message(self.Submitted(self.value))
            self.value = ""
            self.cursor = 0
            self.suggestion = ""
            event.stop()
            self.refresh()
            return

        if key == "left" and self.cursor > 0:
            self.cursor -= 1
            event.stop()
            return

        if key == "right" and self.cursor < len(self.value):
            self.cursor += 1
            event.stop()
            return

        if key == "backspace" and self.cursor > 0:
            self.value = self.value[:self.cursor - 1] + self.value[self.cursor:]
            self.cursor -= 1
            input_changed = True
            event.stop()

        elif char and char.isprintable():
            self.value = self.value[:self.cursor] + char + self.value[self.cursor:]
            self.cursor += 1
            input_changed = True
            event.stop()

        if input_changed:
            self.refresh()

            # if self.suggestion_timer:
            #     self.suggestion_timer.stop()

            # self.suggestion_timer = self.set_timer(0.4, lambda: self.run_suggestion())

    def update_prompt(self, context_name: str):
        self.prompt = f"[{context_name}] "

    def run_suggestion(self):
        if not self.value or len(self.value.strip()) < 2:
            self.suggestion = ""
            self.refresh()
            return

        suggestion = get_prompt_suggestion(self.value, resource_cache)
        if suggestion.lower().startswith(self.value.lower()):
            self.suggestion = suggestion
        else:
            self.suggestion = ""
        self.refresh()
