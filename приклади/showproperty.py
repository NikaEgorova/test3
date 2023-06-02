# у програмі описаний клас MyInput - це TextInput, який зберігає
# властивість mytext. При зміні тексту ця властивість також змінюється
# (це перевернутий текст, але зовні віджету ми не повинні знати алгоритм).
# Далі створюється інтерфейс, в якому обробляється зміна властивості mytext:
# щоразу при зміні ця властивість відображається на label
# див. рядки 15, 21, 28, 33

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

class MyInput(TextInput):
    mytext = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self.changevalue)
    
    def changevalue(self, widget, value):
        self.mytext = "".join(reversed(self.text))

class MyBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.txt_in = MyInput(size_hint_y=None, height="30sp")
        self.label = Label()
        self.txt_in.bind(mytext=self.textchanged)
        self.add_widget(self.txt_in)
        self.add_widget(self.label)

    def textchanged(self, widget, value):
        self.label.text = "Що? " + value + " ?"

class MyApp(App):
    def build(self):
        box = MyBox()
        return box


app = MyApp()
app.run()