"""This doesn't work properly. It's just a starting point."""

import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView


class FileExplorer(BoxLayout):
    def __init__(self, **kwargs):
        super(FileExplorer, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.url_bar = TextInput(hint_text="Enter URL", multiline=False, readonly=True)
        self.add_widget(self.url_bar)

        self.tree_view = FileChooserIconView(path=os.path.expanduser("~"))
        self.tree_view.bind(on_submit=self.update_file_list)
        self.add_widget(self.tree_view)

        self.file_list = ScrollView()
        self.add_widget(self.file_list)

        self.file_list_layout = BoxLayout(orientation="vertical")
        self.file_list.add_widget(self.file_list_layout)

        self.update_file_list(self.tree_view.path)

    def update_file_list(self, path):
        self.url_bar.text = path
        self.file_list_layout.clear_widgets()

        files = os.listdir(path)
        for file in files:
            file_label = Label(text=file, size_hint_y=None, height=40)
            self.file_list_layout.add_widget(file_label)


class FileExplorerApp(App):
    def build(self):
        return FileExplorer()


if __name__ == "__main__":
    FileExplorerApp().run()
