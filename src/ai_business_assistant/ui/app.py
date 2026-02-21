from dataclasses import field

import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30

    def animate(e: ft.Event[ft.Button]):
        container.scale = 2 if container.scale == 1 else 1
        page.update()

    page.add(
        container := ft.Container(
            width=100,
            height=100,
            bgcolor=ft.Colors.LIGHT_BLUE,
            border_radius=5,
            scale=1,
            animate_scale=ft.Animation(
                duration=600,
                curve=ft.AnimationCurve.BOUNCE_OUT,
            ),
        ),
        ft.Button("Animate!", on_click=animate),
    )

def run():
    # simplest local run; for Codespaces you’ll likely use CLI flags (--web, --port)
    ft.app(target=main)

if __name__ == "__main__":
    run()

#def main(page: ft.Page):
#    page.title = "AI Business Assistant"
#    page.add(ft.Text(" Iniciando una gran Historia... 👋"))

#def run():
    # simplest local run; for Codespaces you’ll likely use CLI flags (--web, --port)
#    ft.app(target=main)

#if __name__ == "__main__":
#    run()