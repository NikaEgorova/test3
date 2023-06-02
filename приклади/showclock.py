# програма з трьома екранами, перемикання на третій екран відбувається за таймером
# таймер включається у методі on_enter другого екрана, тобто. відразу після того, як користувач зайшов на цей екран
# Див. рядок 58
 
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

time_to_read = 5
long_txt = """Використовуйте ці поради, щоб збільшити швидкість читання:\n
1. Не промовляйте текст, що читається.\n
Якщо звичка промовляти вже є, тренуйтеся читати і одночасно співати із закритими губами одну ноту.\n
2. Вчіться схоплювати поглядом відразу кілька слів.\n
Тренуйтеся, кидаючи погляд на текст. Не переміщуючи погляду, закрийте очі та відновіть у пам'яті, що встигли прочитати.\n
3. Досягніть руху погляду зверху вниз.\n
Не повертайте погляду на вже прочитане. Тренуйтеся, читаючи вузькі колонки тексту.\n
Можна допомагати собі, рухаючи по тексту аркуш паперу, щоб він закривав верхню частину сторінки. Прискорюйте рух аркуша.\n
4. Зосередьте увагу на читанні.\n
Читайте довгі тексти. Заберіть відволікаючі фактори. Шукайте книги, які вас захоплять. """

# клас для акуратного відображення довгого тексту на маленькому екрані з прокручуванням
# детальніше ти можеш прочитати в документації до першого уроку

class ScrollLabel(ScrollView):
    def __init__(self, ltext, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text=ltext, markup=True, size_hint_y=None, font_size='20sp', halign='left', valign='top')
        self.label.bind(size=self.resize)
        self.add_widget(self.label)

    def resize(self, *argv):
        self.label.text_size = (self.label.width, None)
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]

class FirstScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=10)
        box.add_widget(Label(text="Спробуйте прочитати текст за " + str(time_to_read) + " секунд(и)"))
        btn_next = Button(text="Почати", on_press=self.next)
        box.add_widget(btn_next)
        self.add_widget(box) 

    def next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'showtext' 

class ShowText(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(padding=10)
        box.add_widget(ScrollLabel(long_txt, size_hint_x=0.8, pos_hint={'center_x':0.5})) 
        self.add_widget(box)
    
    def on_enter(self):
        Clock.schedule_once(self.next, time_to_read)

    def next(self, dt):
        print("Пройшло", dt, "секунд")
        self.manager.current = 'last' 

class LastScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Час!")) 

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScr(name='1'))
        sm.add_widget(ShowText(name='showtext'))
        sm.add_widget(LastScr(name='last'))
        return sm

app = MyApp()
app.run()
