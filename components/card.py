import flet as ft

def create_card_content(direction_text, card_text, show_front, on_click=None):
    return ft.Container(
        content=ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [direction_text, card_text],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=30,
                alignment=ft.alignment.center,
            ),
        ),
        width=400,
        height=200,
        bgcolor=ft.colors.WHITE,
        on_click=on_click,  # Add click handler here
    )

def create_card_container(direction_text, card_text, on_click):
    return ft.AnimatedSwitcher(
        content=create_card_content(direction_text, card_text, True, on_click),
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=300,
        reverse_duration=300,
        switch_in_curve=ft.AnimationCurve.EASE_IN,
        switch_out_curve=ft.AnimationCurve.EASE_OUT,
    )

def create_input_controls():
    guess_input = ft.TextField(
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

    switch_btn = ft.ElevatedButton(
        text="Switch Languages",
        width=300,
    )

    return guess_input, submit_btn, next_btn, switch_btn