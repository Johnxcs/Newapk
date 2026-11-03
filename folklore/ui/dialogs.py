"""Folklore popup dialog with a queue so dialogs never overlap."""

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView


class FolkloreDialogManager:
    def __init__(self, theme_cls):
        self.theme_cls = theme_cls
        self.dialog = None
        self.queue = []

    def show(self, site):
        self.queue.append(site)
        self._show_next()

    def _show_next(self):
        if self.dialog is not None or not self.queue:
            return
        site = self.queue.pop(0)

        content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(300),
            spacing=dp(8),
        )
        content.add_widget(
            MDLabel(
                text=site.legend_title,
                font_style="Subtitle1",
                bold=True,
                theme_text_color="Custom",
                text_color=self.theme_cls.accent_color,
                adaptive_height=True,
            )
        )
        scroll = MDScrollView()
        scroll.add_widget(MDLabel(text=site.story, adaptive_height=True))
        content.add_widget(scroll)

        self.dialog = MDDialog(
            title=f"{site.name} - {site.place}",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="CLOSE", on_release=self._close)],
            on_dismiss=self._on_dismiss,
        )
        self.dialog.open()

    def _close(self, *_):
        if self.dialog:
            self.dialog.dismiss()

    def _on_dismiss(self, *_):
        self.dialog = None
        Clock.schedule_once(lambda _dt: self._show_next(), 0.3)
