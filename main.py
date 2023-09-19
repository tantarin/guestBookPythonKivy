# import all the relevant classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text

import pandas as pd


# class to call the popup function
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class GuestEntry(Base):
    __tablename__ = 'guest_entries'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    comment = Column(Text)

class PopupWindow(Widget):
    def btn(self):
        popFun()


# class to build GUI for a popup window
class P(FloatLayout):
    pass


# function that displays the content
def popFun():
    show = P()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


class messagesWindow(Screen):
    def on_pre_enter(self):
        entries = self.session.query(GuestEntry).all()
        message_text = ""
        for entry in entries:
            message_text += f"Имя: {entry.name}\nEmail: {entry.email}\nСообщение: {entry.comment}\n\n"
        self.ids.messages_label.text = message_text



class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    message = ObjectProperty(None)

    def signupbtn(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)  # Используем SQLite в памяти
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        name2 = self.name2.text if self.name else ""  # Проверка наличия имени
        email = self.email.text if self.email else ""  # Проверка наличия email
        message = self.message.text if self.message else ""  #
        if name2 and message:
            # добавляем в бд
            new_entry = GuestEntry(name=name2, email=email, comment=message)  # Сохраняем email
            self.session.add(new_entry)
            self.session.commit()
            # Очищаем поля
            self.name2.text = ''
            self.email.text = ''
            self.message.text = ''
        entries = self.session.query(GuestEntry).all()
        print(entries)
        sm.get_screen('messages').session = self.session
        sm.current = 'messages'


# class to display validation result
class logDataWindow(Screen):
    pass


# class for managing screens
class windowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file('guestbook.kv')
sm = windowManager()


class loginMain(App):
    def build(self):
        signup_window = signupWindow(name='signup')
        messages_window = messagesWindow(name='messages')
        sm.add_widget(signup_window)
        sm.add_widget(messages_window)
        return sm


# driver function
if __name__ == "__main__":
    loginMain().run()
