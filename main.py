from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
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
    def on_pre_enter(self): #действия перед показом экрана
        self.ids.messages_grid.clear_widgets()
        if hasattr(self, 'session'):
            entries = session.query(GuestEntry).all()
            for entry in entries:
                name_and_email = f'{entry.name}, {entry.email}'
                comment_text = entry.comment
                name_email_label = Button(text=name_and_email)
                comment_label = Button(text=comment_text)
                name_email_label.color = (1, 0, 0, 1)
                name_email_label.size_hint_x = 0.3
                comment_label.size_hint_x = 0.7
                self.ids.messages_grid.add_widget(name_email_label)
                self.ids.messages_grid.add_widget(comment_label)


class addWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    message = ObjectProperty(None)

    def addbtn(self):
        name2 = self.name2.text if self.name else ""
        email = self.email.text if self.email else ""
        message = self.message.text if self.message else ""
        if name2 and message and email:
            new_entry = GuestEntry(name=name2, email=email, comment=message)
            session.add(new_entry)
            session.commit()
            self.name2.text = ''
            self.email.text = ''
            self.message.text = ''
        sm.get_screen('messages').session = session
        sm.current = 'messages'


class windowManager(ScreenManager):
    pass


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

kv = Builder.load_file('guestbook.kv')
sm = windowManager()


class main(App):
    def build(self):
        add_window = addWindow(name='add')
        messages_window = messagesWindow(name='messages')
        sm.add_widget(add_window)
        sm.add_widget(messages_window)
        return sm


if __name__ == "__main__":
    main().run()
