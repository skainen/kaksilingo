import flet as ft

class CardDisplay(ft.UserControl):
    def __init__(self, text: str, on_click):
        super().__init__()
        self.text = text
        self.on_click = on_click

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Text(
                    value=self.text,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=20,
                alignment=ft.alignment.center,
            ),
            width=400,
            height=200,
            on_click=self.on_click
        )