import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from loguru import logger
from kivy.config import Config




Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')



#Aqui estoy configurando el teclado del movil
# # Window.keyboard_anim_args = {'d':.2,'t':'in_out_expo'}
# # Window.softinput_mode = "below_target"



class Organizador(App):
    #Inicializo con esta clase, la cual hereda la clase App de Kivy.

    
    screen_manager = ScreenManager()

    # Agregar las pantallas Acceder y Registro al ScreenManager
    
    

    



    
    def build(self,screen_manager=screen_manager):
        
        
        #Este es el primer metodo que se ejecuta en una app de kivy
        
        Builder.load_file('Diseño.kv')
        
        self.InicializarScreens(screen_manager)
        
        screen_manager.current = 'acceder'
        Window.size = (400, 600)
        
        return screen_manager
    

    
    def InicializarScreens( screen_manager):
        acceder_screen = Screen(name='acceder')
        acceder_screen.add_widget(Acceder())
        screen_manager.add_widget(acceder_screen)

        registro_screen = Screen(name='registro')
        registro_screen.add_widget(Registro())
        screen_manager.add_widget(registro_screen)
        
        return screen_manager
        
    

    def PantallaRegistro(self,screen_manager=screen_manager):
        
        screen_manager.current = 'registro'




class Registro(Screen):
    None
class Acceder(Screen):
    
    None
if __name__ == '__main__':
    try:
        Organizador().run()
    except Exception as e:
        logger.error(e)