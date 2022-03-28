from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import pymongo


cbh1=False
cbh2=False
cbh3=False
cbh4=False
# Create the client
client = pymongo.MongoClient('mongodb://localhost:27017/')

# Connect to our database
db = client['qestion']

# Fetch our series collection
collection = db['test']




#screens
class ScreenManagement(ScreenManager):
    pass


class MenuScreen(Screen):

    def save_setting(self,widget):

        if ((cbh1 or cbh2) and (cbh3 or cbh4)) and (self.ids["input"].text != ''):

            data = {
                'q1': False,
                'q2':False,
                'q3':f'{self.ids["input"].text}'
            }

            if cbh1:
                data['q1'] = True
            if cbh3:
                data['q2'] = True
            collection.insert_one(data)
        else:
            layout = GridLayout(cols=1, padding=10)
            popupLabel = Label(text="Некорректный ввод")
            closeButton = Button(text="Закрыть")
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            # Instantiate the modal popup and display
            popup = Popup(title='Ошибка',
                          content=layout,
                          size_hint=(None, None), size=(200, 200))
            popup.open()

            # Attach close button press with popup.dismiss action
            closeButton.bind(on_press=popup.dismiss)
            return



    def check_box_hendler1(self, widget, value):
        global cbh1
        cbh1 = value
    def check_box_hendler2(self, widget, value):
        global cbh2
        cbh2 = value
    def check_box_hendler3(self, widget, value):
        global cbh3
        cbh3 = value
    def check_box_hendler4(self, widget, value):
        global cbh4
        cbh4 = value
    def res(self, widget):

        proc_nice = round(collection.count_documents({'q1':True})*100/collection.count_documents({}),1)
        proc_buy = round(collection.count_documents({'q2':True})*100/collection.count_documents({}),1)
        layout = GridLayout(cols=1, padding=10)
        popupLabel = Label(text=f"понравилось {proc_nice}%\n"
                                f"Купили бы {proc_buy}%")
        closeButton = Button(text="Закрыть")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        # Instantiate the modal popup and display
        popup = Popup(title='Результаты',
                      content=layout,
                      size_hint=(None, None), size=(200, 200))
        popup.open()

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press=popup.dismiss)



class CianApp(App):
    def on_start(self):
        pass


    def on_stop(self):
        pass
        return True





if __name__ == '__main__':
    CianApp().run()