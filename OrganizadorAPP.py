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
        
        screen_manager = self.InicializarScreens(screen_manager)

        

        self.url="https://organizador-5de77-default-rtdb.europe-west1.firebasedatabase.app/.json"
        self.key= "DDG9a9IkOp9ZtvtbhmU0BPJacoBfSxsb4KglypP6"
        
        screen_manager.current = 'acceder'

        

        Window.size = (400, 600)
        
        return screen_manager
    
    
    
    def InicializarScreens(self,screen_manager):
        acceder_screen = Screen(name='acceder')
        acceder_screen.add_widget(Acceder())
        screen_manager.add_widget(acceder_screen)

        registro_screen = Screen(name='registro')
        registro_screen.add_widget(Registro())
        screen_manager.add_widget(registro_screen)
        


        return screen_manager
        
    

    def register_user(self, username_input,email_input,password_input):
        logger.info('Tu usuario es: ' + str(username_input)+' tu email: '+str(email_input)+' y tu contraseña: '+ str(password_input))


 

class Registro(Screen):
    screen_manager = Organizador().screen_manager
    def PantallaInicio(self,screen_manager=screen_manager):
        #Esta clase se ejecuta para cambiar de la pantalla registro a acceder, elimina los campos para que 
        #Vuelvan a quedar en blanco.
        
        self.ids.password_input.text = ''
        self.ids.email_input.text = ''
        self.ids.username_input.text = ''
        
        # logger.info('Entra')
        
        
        screen_manager.current = 'acceder'
        return screen_manager

class Acceder(Screen):
    screen_manager = Organizador().screen_manager
    
    def PantallaRegistro(self,screen_manager=screen_manager):
        #Esta clase se ejecuta para cambiar de la pantalla acceder a registro, elimina los campos para que 
        #Vuelvan a quedar en blanco.
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''


        screen_manager.current = 'registro'

if __name__ == '__main__':
    try:
        Organizador().run()

    except Exception as e:
        logger.error(e)