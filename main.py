# import all the relevant classes
from kivy.app import App
from kivy.core.text.markup import MarkupLabel
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text
from kivy.uix.label import Label
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


class messagesWindow(Screen):
    def on_pre_enter(self):
        self.ids.messages_grid.clear_widgets()  # Очистить содержимое
        if hasattr(self, 'session'):
            entries = session.query(GuestEntry).all()
            for entry in entries:
                # Создаем Label с размеченным текстом и указываем цвет
                message_text = (
                    f'[color=ff0000]Имя:[/color] [color=ffffff]{entry.name}[/color]\n'
                    f'[color=ff0000]Email:[/color] [color=ffffff]{entry.email}[/color]\n'
                    f'[color=ff0000]Сообщение:[/color] [color=ffffff]{entry.comment}[/color]\n\n'
                )
                label = Label(markup=True, text=message_text, halign='left', valign='top')
                self.ids.messages_grid.add_widget(label)




class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    message = ObjectProperty(None)

    def signupbtn(self):
        name2 = self.name2.text if self.name else ""  # Проверка наличия имени
        email = self.email.text if self.email else ""  # Проверка наличия email
        message = self.message.text if self.message else ""  #
        if name2 and message:
            # добавляем в бд
            new_entry = GuestEntry(name=name2, email=email, comment=message)  # Сохраняем email
            session.add(new_entry)
            session.commit()
            # Очищаем поля
            self.name2.text = ''
            self.email.text = ''
            self.message.text = ''
        entries = session.query(GuestEntry).all()
        print(entries)
        sm.get_screen('messages').session = session
        sm.current = 'messages'


# class to display validation result
class logDataWindow(Screen):
    pass


# class for managing screens
class windowManager(ScreenManager):
    pass


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

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
