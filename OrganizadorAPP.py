import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from loguru import logger

#Aqui estoy configurando el teclado del movil
# # Window.keyboard_anim_args = {'d':.2,'t':'in_out_expo'}
# # Window.softinput_mode = "below_target"

class Organizador(App):
    #Inicializo con esta clase, la cual hereda la clase App de Kivy.

    def build(self):
        #Este es el primer metodo que se ejecuta en una app de kivy
       
       
       
        Builder.load_file("Diseño.kv")
        
        return Acceder()
    
    
    def show_register_screen(self):
        







class Registro(BoxLayout):
    None
class Acceder(BoxLayout):
    None

if __name__ == '__main__':
    try:
        Organizador().run()
    except Exception as e:
        logger.error(e)