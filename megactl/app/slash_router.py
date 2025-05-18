from megactl.k8s.context import get_kube_contexts
from megactl.tui.context_selector import ContextSelector
from textual.app import App
from textual.widgets import Static

class CommandHandler:
    def __init__(self, app: App, chat_display: Static, input_box):
        self.app = app
        self.chat = chat_display
        self.input_box = input_box

    async def handle(self, user_input: str) -> bool:
        if user_input == "/history":
            if not self.app.history.history:
                self.chat.add_bot_message("📜 No history available.")
            else:
                self.chat.add_bot_message("📜 Last commands:")
                for cmd in reversed(self.app.history.history[-10:]):
                    self.chat.add_bot_message(f"• {cmd}")
            return True

        elif user_input == "/clear":
            self.chat.clear_display()
            self.chat.add_bot_message("🧹 Screen cleared.")
            return True

        elif user_input.startswith("/use"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                self.app.kube_context = parts[1].strip()
                self.input_box.update_prompt(self.app.kube_context)
                self.chat.add_bot_message(f"🔁 Kubernetes context set to [bold]{self.app.kube_context}[/bold].")
            elif len(parts) == 1:
                contexts = get_kube_contexts()
                if not contexts:
                    self.chat.add_bot_message("❌ Failed to retrieve contexts.")
                else:
                    selector = ContextSelector(contexts)
                    await self.app.push_screen(selector)


            else:
                self.chat.add_bot_message("⚠️ Usage: /use <context> or /use to select one.")
            return True
        
        elif user_input == "/help":
            self.chat.add_bot_message("""📘 Available commands:
• `/use <context>` — switch Kubernetes context
• `/history` — show recent commands
• `/clear` — clear command history
• `/help` — show this help message
""")
            return True

        elif user_input == "/exit":
            self.app.exit()
            return True

        return False
