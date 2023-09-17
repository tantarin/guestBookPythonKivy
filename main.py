from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GuestEntry(Base):
    __tablename__ = 'guest_entries'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    comment = Column(Text)


class GuestBookApp(App):
    def build(self):
        self.engine = create_engine('sqlite:///:memory:')  # Используем SQLite в памяти
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.layout = GridLayout(cols=2)

        self.layout.add_widget(Label(text='Имя:'))
        self.name_input = TextInput()
        self.layout.add_widget(self.name_input)

        self.layout.add_widget(Label(text='Email:'))
        self.email_input = TextInput()
        self.layout.add_widget(self.email_input)

        self.layout.add_widget(Label(text='Комментарий:'))
        self.comment_input = TextInput()
        self.layout.add_widget(self.comment_input)

        self.add_button = Button(text='Добавить')
        self.add_button.bind(on_press=self.add_entry)
        self.layout.add_widget(self.add_button)

        return self.layout

    def add_entry(self, *args):
        name = self.name_input.text
        email = self.email_input.text
        comment = self.comment_input.text
        if name and comment:
            new_entry = GuestEntry(name=name, email=email, comment=comment)  # Сохраняем email
            self.session.add(new_entry)
            self.session.commit()
            self.name_input.text = ''
            self.email_input.text = ''  # Очищаем поле для email
            self.comment_input.text = ''
            self.display_entries()

    def display_entries(self):
        entries = self.session.query(GuestEntry).all()
        entry_text = ''
        for entry in entries:
            entry_text += f'Имя: {entry.name}\nEmail: {entry.email}\nКомментарий: {entry.comment}\n\n'
        self.entry_display.text = entry_text


if __name__ == '__main__':
    GuestBookApp().run()
