from rich.panel import Panel

from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from dataclasses import dataclass

@dataclass
class Message:
    text: str
    is_me: bool


# DB Layer
users = ["Alice", "Bob", "Charlie"]
current_user = "Alice"
messages_by_user = {
    "Alice": [],
    "Bob": [],
    "Charlie": [],
}


class Contacts(Widget):
    def render(self) -> Panel:
        text = ""
        for user in users:
            text += f"- {user}\n"
        return Panel(text)

class Conversation(Widget):
    text = Reactive("")
    def render(self) -> Panel:
        messages = messages_by_user[current_user]
        text = "--"
        for message in messages:
            text += f"{message.text}\n"
        return Panel(text)

class TextInputField(Widget):
    mouse_over = Reactive(False)
    text = Reactive("")

    def render(self) -> Panel:
        if self.mouse_over:
            return Panel(self.text, style="on red")
        else:
            return Panel(self.text)

    def on_key(self, event) -> None:
        if event.key == "enter":
            self.text = ""
            messages_by_user[current_user].append(Message(self.text, is_me=True))
        elif event.key == "ctrl+h":
            self.text = self.text[:-1]
        else:
            self.text += event.key

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False



class HoverApp(App):
    """Demonstrates custom widgets"""

    async def on_mount(self) -> None:
        await self.view.dock(Contacts(), edge="left", size=40)
        await self.view.dock(Conversation(), TextInputField(), edge="top", size=40)


HoverApp.run(log="textual.log")