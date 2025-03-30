from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText


class App(MDApp):
	def build(self):
		self.theme_cls.theme_style = 'Dark'
		self.theme_cls.primary_palette = 'Red'

		return (
			MDScreen(
				MDButton(
					MDButtonText(
						text='Hello, World',
					),
					pos_hint={'center_x': 0.5, 'center_y': 0.5},
				)
			)
		)