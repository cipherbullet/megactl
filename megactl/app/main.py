from pathlib import Path

from textual.app import App, ComposeResult

from megactl.ai.intent_extractor import get_k8s_intent
from megactl.k8s.schema import Intent
from megactl.k8s.executor import execute_kubectl_command
from megactl.k8s.cluster import fetch_cluster_context

from megactl.tui.prompt_input import PromptInput
from megactl.app.history_manager import HistoryManager
from megactl.app.slash_router import CommandHandler
from megactl.tui.layout import build_main_layout
from megactl.tui.chat_display import ChatDisplay
from megactl.ai.intent_extractor import retry_intent_with_error
from megactl.tui.context_selector import ContextSelector


HISTORY_FILE = Path.home() / ".megactl" / "history.json"

class MegaCtlApp(App):
    CSS_PATH = "../../style.css"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kube_context = None
        self.history = HistoryManager(HISTORY_FILE)
        self.command_handler = None

    def compose(self) -> ComposeResult:
        self.input_box = PromptInput(id="input-box")
        yield build_main_layout(self.input_box)

    async def on_mount(self) -> None:
        self.history.load()
        fetch_cluster_context()
        self.set_interval(30, fetch_cluster_context)
        self.command_handler = CommandHandler(self, self.query_one("#chat"), self.input_box)
        self.input_box.focus()

    async def on_prompt_input_submitted(self, message: PromptInput.Submitted) -> None:
        chat = self.query_one("#chat")
        user_input = message.value.strip()
        self.input_box.value = ""

        if not user_input:
            return

        if user_input.startswith("/") and await self.command_handler.handle(user_input):
            return
        
        chat.add_user_message(user_input)
        self.history.append(user_input)
        self.history.save()

        try:
            intent_dict = get_k8s_intent(user_input)
            intent = Intent(**intent_dict)

            if self.kube_context and "--context" not in intent.kubectl:
                intent.kubectl = intent.kubectl.strip() + f" --context={self.kube_context}"


            chat.add_bot_message(f"🚀 {intent.kubectl}")
            code, out, err = execute_kubectl_command(intent.kubectl)

            if code == 0:
                chat.add_output(out, success=True)
            else:
                chat.add_output(err, success=False)

                # 🧠 Retry with GPT using error context
                chat.add_bot_message("⚠️ Trying to correct the command based on the error...")
                retry = retry_intent_with_error(user_input, err)
                chat.add_bot_message(f"🔁 Retrying: {retry['kubectl']}")
                code2, out2, err2 = execute_kubectl_command(retry["kubectl"])
                chat.add_output(out2 if code2 == 0 else err2, success=(code2 == 0))

        except Exception as e:
            chat.add_bot_message(f"❌ {e}")
        finally:
            self.input_box.focus()

    def on_key(self, event) -> None:
        if event.key == "up":
            previous = self.history.back()
            if previous:
                self.input_box.value = previous
        elif event.key == "down":
            next_entry = self.history.forward()
            self.input_box.value = next_entry
        elif event.key == "ctrl+l":
            self.query_one("#chat", ChatDisplay).clear_display()
            event.stop()

    async def on_context_selector_context_selected(self, message: ContextSelector.ContextSelected) -> None:
        self.kube_context = message.context_name
        self.input_box.update_prompt(self.kube_context)
        chat = self.query_one("#chat")
        chat.add_bot_message(f"✅ Context switched to [bold]{self.kube_context}[/bold]")


def main():
    app = MegaCtlApp()
    app.run()

if __name__ == "__main__":
    main()
