import flet as ft

def create_card_container(card_subtitle, card_text):
    return ft.Container(
        content=ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [card_subtitle, card_text],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=30,
                alignment=ft.alignment.center,
            ),
        ),
        animate=ft.animation.Animation(300, "easeInOut"),
        width=400,
        height=200,
        bgcolor=ft.colors.WHITE,
        scale=ft.transform.Scale(1, alignment=ft.alignment.center),
    )

def create_input_controls():
    guess_input = ft.TextField(
        label="Finnish translation",
        width=300,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    submit_btn = ft.ElevatedButton(
        text="Submit",
        visible=False,
        width=300,
    )

    next_btn = ft.ElevatedButton(
        text="Next Word",
        visible=False,
        width=300,
    )

    return guess_input, submit_btn, next_btn