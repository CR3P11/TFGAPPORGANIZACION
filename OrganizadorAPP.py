import kivy #Es la libreria principal de la aplicacion, sirve para desarrollar aplicaciones con python: https://kivy.org/doc/stable/
import requests #Es una libreria para hacer solicitudes http: https://requests.readthedocs.io/en/latest/
import json #Libreria para el manejo y gestion de los ficheros json.
import datetime #Libreria para el manejo de fechas
from validate_email import validate_email #La voy a utilizar para verificar el email. Es una libreria que permite comparar cadenas.
kivy.require('2.1.0') #La version de esta app requiere kivy 2.1 o superior.

'''
Para instalar las dependencias utilizaremos los siguientes comandos en la cmd con el pip:

pip install kivy
pip install requests
pip install validate_email

Todas las librerias son necesarias para el correcto funcionamiento de la aplicación.

'''


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from loguru import logger
from kivy.config import Config
from kivy.properties import ListProperty
from kivy.uix.label import *
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')



#Aqui estoy configurando el teclado del movil
# # Window.keyboard_anim_args = {'d':.2,'t':'in_out_expo'}
# # Window.softinput_mode = "below_target"



class Organizador(App):
    #Inicializo con esta clase, la cual hereda la clase App de Kivy.

    
    screen_manager = ScreenManager()

    # Agregar las pantallas Acceder y Registro al ScreenManager


    url="https://organizador-5de77-default-rtdb.europe-west1.firebasedatabase.app/.json"
    key= "DDG9a9IkOp9ZtvtbhmU0BPJacoBfSxsb4KglypP6"
        


    
    def build(self,screen_manager=screen_manager):
        
        #Este es el primer metodo que se ejecuta en una app de kivy
        
        Builder.load_file('Diseño.kv')
        
        screen_manager = self.InicializarScreens(screen_manager)

        

        
        # screen_manager.current = 'acceder'
        screen_manager.current = 'principal'

        

        Window.size = (400, 600)
        
        return screen_manager
    
    def pantallaPrincipal(self):
        self.screen_manager.current = 'principal'
    
    def InicializarScreens(self,screen_manager):
        acceder_screen = Screen(name='acceder')
        acceder_screen.add_widget(Acceder())
        screen_manager.add_widget(acceder_screen)

        registro_screen = Screen(name='registro')
        registro_screen.add_widget(Registro())
        screen_manager.add_widget(registro_screen)

        principal_screen = Screen(name='principal')
        principal_screen.add_widget(PantallaPrincipal())
        screen_manager.add_widget(principal_screen)
        
        calendar_screen = Screen(name='calendario')
        calendar_screen.add_widget(PantallaCalendario())
        screen_manager.add_widget(calendar_screen)

        contact_screen = Screen(name='contactos')
        contact_screen.add_widget(PantallaContactos())
        screen_manager.add_widget(contact_screen)

        backpack_screen = Screen(name='mochila')
        backpack_screen.add_widget(PantallaMochila())
        screen_manager.add_widget(backpack_screen)

        settings_screen = Screen(name='ajustes')
        settings_screen.add_widget(PantallaAjustes())
        screen_manager.add_widget(settings_screen)

        notes_screen = Screen(name='notas')
        notes_screen.add_widget(PantallaNotas())
        screen_manager.add_widget(notes_screen)

        show_notes_screen = Screen(name='MostrarNotas')
        show_notes_screen.add_widget(PantallaMostrarNotas())
        screen_manager.add_widget(show_notes_screen)



        return screen_manager
        
    
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
    
    
    
    
    def register_user(self,user,email,password,password2):
        url = Organizador().url
        key = Organizador().key

        state = 'Datos incorrectos'
        data = requests.get(url+'?auth='+key) 

        logger.debug(data)
        
        if password != password2:
            state = 'No coinciden las contraseñas'
        elif len(user)<=4:
            state = 'Usuario muy corto'
        elif len(password)<=4:
            state = 'Contraseña muy corta'
        elif validate_email(email) != True:
            state = 'Email incorrecto'
        else:
            for key,value in data.json().items():
                userj= value['User']
                if userj == user:
                    state = 'El usuario exite'
                    break
            if userj != user:
                send_data = {user:{'User':user,'Password':password,'Email':email}}
                requests.patch(url=url,json=send_data)
                state = 'Usuario registrado correctamente'
        
        self.ids.password_input.text = ''
        self.ids.email_input.text = ''
        self.ids.username_input.text = ''
        self.ids.Señal_Registro.text = state
        
        return state

class Acceder(Screen):
    screen_manager = Organizador().screen_manager
    
    def PantallaRegistro(self,screen_manager=screen_manager):
        #Esta clase se ejecuta para cambiar de la pantalla acceder a registro, elimina los campos para que 
        #Vuelvan a quedar en blanco.
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''


        screen_manager.current = 'registro'
    
    
    
    
    
    
    
    
    def login_user(self,user,password):
        
        url = Organizador().url
        key = Organizador().key

        logger.debug(url + " "+key)

        state = False
        data = requests.get(url+'?auth='+key) 
        #Con esto obtengo el json de la base de datos la cual se iterará sobre el siguiente bucle

        for key,value in data.json().items():
            user_reg = value['User']
            password_reg = value['Password']

            if user == user_reg:
                if password == password_reg:
                    state = True
                    self.ids.Señal_Inicio.text = 'Usuario aceptado'
                else:
                    self.ids.password_input.text = '' 
                    self.ids.Señal_Inicio.text = 'Contraseña Incorrecta'
            else:
                self.ids.password_input.text = '' 
                self.ids.username_input.text = '' 
                self.ids.Señal_Inicio.text = 'Usuario Incorrecto'
        return state



class PantallaPrincipal(Screen):
    screen_manager = Organizador().screen_manager
    def pantallanotas(self):
        self.screen_manager.current = 'notas'
    def pantallacontactos(self):
        self.screen_manager.current = 'contactos'
    def pantallamochila(self):
        self.screen_manager.current = 'mochila'
    def pantallaAjustes(self):
        self.screen_manager.current = 'ajustes'
    def pantallacalendario(self):
        self.screen_manager.current = 'calendario'





class PantallaNotas(Screen):

    screen_manager = Organizador().screen_manager

    def mostrarNotas(self):
        self.screen_manager.current = 'MostrarNotas'
        

    
    
    def borrar(self):
        self.ids.text_input.text = ''
        self.ids.tittle.text = ''

    

    def añadir_nota(self, titulo, contenido):
        
        if len(titulo)>=16:
            titulo = titulo[:16]
        if len(contenido)>=600:
            contenido = contenido[:600]
        contenido = "\n".join([contenido[i:i+30] for i in range(0, len(contenido), 30)])
            

        now = datetime.datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        data = {}
        try:
            with open('notas.json', 'r') as infile:
                data = json.load(infile)
        except FileNotFoundError:
            pass  # Si el archivo no existe, se creará uno nuevo a continuación
        
        if fecha in data:
            data[fecha][titulo] = {"titulo": titulo, "contenido": contenido}
        else:
            data[fecha] = {titulo: {"titulo": titulo, "contenido": contenido}}

        with open('notas.json', 'w') as outfile:
            json.dump(data, outfile)



class PantallaMochila(Screen):

    def mochilas():
        pass
    def actualizar_mochila():
        pass



    def borrar(self):
        pass

class PantallaContactos(Screen):
    None
class PantallaCalendario(Screen):
    None
class PantallaAjustes(Screen):
    None



class ContenidoScreen(Screen):
    screen_manager = Organizador().screen_manager

    def __init__(self, contenido, **kwargs):
        super().__init__(**kwargs)
        self.contenido = contenido
        self.label = Label(text=contenido)

        self.add_widget(self.label)

    
    def pantallaAnterior(self):

        self.screen_manager.current = 'notas'
        self.screen_manager.remove_widget(self.screen_manager.get_screen('contenido'))

class PantallaMostrarNotas(Screen):
    screen_manager = Organizador().screen_manager
    notas = ListProperty([])
    
    def actualizar_notas(self):
        with open('notas.json') as f:
            notas = json.load(f)

        grid_layout = GridLayout(cols=2, pos_hint={"top": 0.9, "right": 0.9}, size_hint=(0.8, 0.3))
        for fecha, datos in notas.items():
            contenido_label = Label(text=fecha,size_hint=(0.4, 0.3),color=[1, 0, 0, 1],size_hint_x=10)
            for titulo, contenido in datos.items():
                # logger.info(contenido['titulo']+' '+contenido['contenido'])
                contenido_label = Button(text='[b]' +contenido['titulo']+ '[/b]',background_color=[1, 0, 0, 1] , markup=True,strip=True,size_hint=(0.4, 0.3))
                contenido_label.bind(on_press=lambda x, contenido=contenido['contenido']: self.cambiar_a_contenido(contenido))
                grid_layout.add_widget(contenido_label)
        self.add_widget(grid_layout)
        self.grid_layout = grid_layout

    def borrar(self):
        try:
            grid_layout = self.grid_layout
            if grid_layout is not None:
                for widget in grid_layout.children[:]:
                    grid_layout.remove_widget(widget)
        except AttributeError:
            pass
        
    def cambiar_a_contenido(self, contenido):
        content_screen = Screen(name='contenido')
        content_screen.add_widget(ContenidoScreen(contenido))
        self.screen_manager.add_widget(content_screen)

        # Agregar botón para eliminar la nota actual
        borrar_button = Button(text='Eliminar nota', size_hint_y=0.1)
        borrar_button.contenido = contenido
        borrar_button.bind(on_press=self.eliminar_nota)
        content_screen.add_widget(borrar_button)

        self.screen_manager.current = 'contenido'

    def eliminar_nota(self, instance):
        # Eliminar nota actual del archivo JSON
        with open('notas.json', 'r+') as f:
            notas = json.load(f)
            for fecha, datos in notas.items():
                for titulo, contenido in datos.items():
                    if contenido['contenido'] == self.screen_manager.current_screen.children[0].contenido:
                        del datos[titulo]
                        break
                if not datos:
                    # Si no hay más notas para esa fecha, eliminar fecha
                    del notas[fecha]
                    break
            f.seek(0)
            json.dump(notas, f, indent=4)
            f.truncate()

        self.screen_manager.remove_widget(self.screen_manager.current_screen)
        self.screen_manager.current = 'MostrarNotas'
        # Actualizar la lista de notas
        self.borrar()
        self.actualizar_notas()



if __name__ == '__main__':
    try:
        Organizador().run()

    except Exception as e:
        logger.error(e)