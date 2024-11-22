import flet as ft

class AddCardDialog(ft.UserControl):
    def __init__(self, on_save):
        super().__init__()
        self.on_save = on_save
        self.front_input = ft.TextField(label="Front (Word/Phrase)")
        self.back_input = ft.TextField(label="Back (Translation)")
        self.language_input = ft.TextField(label="Language")

    def clear_inputs(self):
        self.front_input.value = ""
        self.back_input.value = ""
        self.language_input.value = ""

    def build(self):
        return ft.AlertDialog(
            title=ft.Text("Add New Flashcard"),
            content=ft.Column([
                self.front_input,
                self.back_input,
                self.language_input
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Add", on_click=self.save_card),
            ]
        )

    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()

    def save_card(self, e):
        self.on_save(
            self.front_input.value,
            self.back_input.value,
            self.language_input.value
        )
        self.clear_inputs()
        self.dialog.open = False
        self.page.update()