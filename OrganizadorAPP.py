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
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

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

        
        self.ColorCanvas("verde", True)

        
        # screen_manager.current = 'acceder'
        # screen_manager.current = 'principal'

        

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
        
        settings_screen = Screen(name='ajustes')
        settings_screen.add_widget(PantallaAjustes())
        screen_manager.add_widget(settings_screen)

        contact_screen = Screen(name='contactos')
        contact_screen.add_widget(PantallaContactos())
        screen_manager.add_widget(contact_screen)

        backpack_screen = Screen(name='mochila')
        backpack_screen.add_widget(PantallaMochila())
        screen_manager.add_widget(backpack_screen)

        notes_screen = Screen(name='notas')
        notes_screen.add_widget(PantallaNotas())
        screen_manager.add_widget(notes_screen)

        show_notes_screen = Screen(name='MostrarNotas')
        show_notes_screen.add_widget(PantallaMostrarNotas())
        screen_manager.add_widget(show_notes_screen)



        return screen_manager
    
    def ColorCanvas(self, color,dentro=True):
        colors = {
            "amarillo": (1, 1, 0),
            "verde": (0, 1, 0),
            "rojo": (1, 0, 0),
            "naranja": (1, 0.5, 0),
            "morado": (0.5, 0, 1),
            "azul": (0, 0, 1),
            "cian": (0, 1, 1),
            "gris": (0.5, 0.5, 0.5),
            "blanco": (1, 1, 1),
            "negro": (0, 0, 0)
        }
        self.screen_manager.canvas.add(Color(*colors[color]))
        self.screen_manager.canvas.add(Rectangle(size=(400, 600)))
        Builder.load_file('Diseño.kv')

        if dentro == True:
            self.screen_manager.current = 'principal'
        elif dentro==False:
            self.screen_manager.current = 'registro'
            self.screen_manager.current = 'acceder'
        # else:
        #     self.screen_manager.current = 'error'
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
    def pantallaAcceder(self):
        self.screen_manager.current = 'acceder'



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
    mochilas = {}
    screen_manager = Organizador().screen_manager
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Cargar las mochilas desde el archivo JSON
        with open('mochilas.json', 'r') as f:
            self.mochilas = json.load(f)
        
        # Crear los botones de las mochilas
        mochilas_layout = self.ids.mochilas_layout
        for nombre_mochila, items in self.mochilas.items():
            mochila_button = Button(
                text=nombre_mochila,
                size_hint_y=None,
                height=dp(40),
                on_release=lambda button: self.mostrar_items_mochila(button.text)
            )
            mochilas_layout.add_widget(mochila_button)
            mochilas_layout.height += mochila_button.height + mochilas_layout.spacing[1]

    def añadir_mochila(self):
        nombre_mochila = self.ids.mochila.text.strip()
        if nombre_mochila:
            self.mochilas[nombre_mochila] = []
            self.ids.mochila.text = ""
            mochilas_layout = self.ids.mochilas_layout
            mochila_button = Button(
                text=nombre_mochila,
                size_hint_y=None,
                height=dp(40),
                on_release=lambda button: self.mostrar_items_mochila(button.text)
            )
            self.ids.mochilas_container.add_widget(mochila_button)
            self.ids.mochilas_container.height += mochila_button.height + mochilas_layout.spacing[1]
            self.ids.mochila.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            self.ids.plus_button.pos_hint = {"center_x": 0.5, "center_y": 0.4}

            with open('mochilas.json', 'w') as f:
                json.dump(self.mochilas, f)
    
    def mostrar_items_mochila(self, nombre_mochila):
        items_screen = Screen(name='items')
        items_screen.add_widget(Items(nombre_mochila,self.mochilas[nombre_mochila]))
        self.screen_manager.add_widget(items_screen)
        
        self.screen_manager.current = 'items'
class Items(Screen):
    screen_manager = Organizador().screen_manager
    items_layout = GridLayout(cols=1, spacing=10, size_hint_y=1)
    
    def __init__(self, mochila, items):
        # Guardar el nombre de la mochila en un atributo
        self.nombre_mochila = mochila
        
        # Crear un GridLayout para los items
        self.items_layout.bind(minimum_height=self.items_layout.setter('height'))
       



        # Añadir un Label con el nombre de la mochila
        mochila_label = Label(text=mochila, font_size=15, bold=True, size_hint=(1, 0.1), pos_hint={"x": 0, "top": 0.95})

        space = Label(text="", size_hint_y=None, height=dp(70))
        self.items_layout.add_widget(space)
        
        if items:
            # Añadir los botones de los items
            for item in items:
                item_button = Button(text=item, size_hint_y=None, height=dp(25),on_release=lambda event, nombre_item=item:self.eliminarItem(nombre_item, mochila,scroll_view, self.items_layout))
                self.items_layout.add_widget(item_button)
        else:
            # Agregar un widget de relleno para asegurarse de que el GridLayout tenga una altura mínima
            filler = Label(text="No hay objetos", size_hint_y=None, height=dp(25))
            self.items_layout.add_widget(filler)
        
        

        self.items_layout.height = len(items) * (dp(40) + self.items_layout.spacing[1])
   
        # Añadir el ScrollView que contendrá los botones de los items
        scroll_view = ScrollView()
        scroll_view.add_widget(self.items_layout)
        super().__init__()
        self.add_widget(mochila_label)
        self.add_widget(scroll_view)
        self.add_widget(Button(text="<", size_hint=(0.15, 0.05), pos_hint={"x": 0, "top": 0.98}, on_release=lambda event: self.pantallaAnterior(scroll_view,self.items_layout)))
        self.add_widget(Button(text="+", size_hint=(0.15, 0.05), pos_hint={"x": 0.80, "top": 0.98}, on_release=lambda event: self.AñadirItems(mochila,scroll_view,self.items_layout)))
    
    def eliminarItem(self, nombre_item, mochila,scroll_view, items_layout):
        # Obtener la lista actual de items de la mochila
        mochilas = json.load(open("mochilas.json", "r"))
        items = mochilas[mochila]
        # Eliminar el item de la lista
        items.remove(nombre_item)
        # Actualizar el JSON
        mochilas[mochila] = items
        with open("mochilas.json", "w") as f:
            json.dump(mochilas, f)
        # Actualizar la pantalla de items
        items_layout.clear_widgets()
        self.borrar(scroll_view,items_layout)
        self.__init__(mochila, items)

        
    
    
    def pantallaAnterior(self,scroll_view,items_layout):
        self.screen_manager.current = 'mochila'
        self.screen_manager.remove_widget(self.screen_manager.get_screen('items'))
        self.borrar(scroll_view,items_layout)


    def AñadirItems(self,mochila,scroll_view,items_layout):
        # Crear un PopUp para introducir el nombre del nuevo item
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        nombre_label = Label(text="Nombre del item:")
        nombre_input = TextInput(multiline=False)
        content.add_widget(nombre_label)
        content.add_widget(nombre_input)
        popup = Popup(title="Agregar item", content=content, size_hint=(0.5, 0.5))
        button_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(40))
        cancel_button = Button(text="Cancelar", on_release=popup.dismiss)
        agregar_button = Button(text="Agregar", on_release=lambda event: self.agregarItem(nombre_input.text, mochila, popup,scroll_view,items_layout))
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(agregar_button)
        content.add_widget(button_layout)
        
        popup.open()
   
    def agregarItem(self, nombre_item, mochila, popup,scroll_view,items_layout):

        
        if len(nombre_item)<1 or len(nombre_item)>40:
            nombre_item = 'error caracteres'
        
        # Obtener la lista actual de items de la mochila
        mochilas = json.load(open("mochilas.json", "r"))
        items = mochilas[mochila]
        # Agregar el nuevo item a la lista
        items.append(nombre_item)
        # Actualizar el JSON
        mochilas[mochila] = items
        with open("mochilas.json", "w") as f:
            json.dump(mochilas, f)
        # Actualizar la pantalla de items
        self.borrar(scroll_view,items_layout)
        self.__init__(mochila, items)
        popup.dismiss()

    def borrar(self,scroll_view,items_layout):
        try:
            if scroll_view is not None:
                for widget in scroll_view.children[:]:
                    scroll_view.remove_widget(widget)
            if items_layout is not None:
                for widget in items_layout.children[:]:
                    items_layout.remove_widget(widget)
                    
        except AttributeError:
            pass    

class PantallaContactos(Screen):
    None



        
class PantallaAjustes(Screen):
    screen_manager = Organizador().screen_manager
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def color(self):
        color_screen = Screen(name='color')
        color_screen.add_widget(SelectColor())
        self.screen_manager.add_widget(color_screen)

        self.screen_manager.current = 'color'
    
    def musica(self):
        music_screen = Screen(name='musica')
        music_screen.add_widget(Musica())
        self.screen_manager.add_widget(music_screen)

        self.screen_manager.current = 'musica'
    
    def ayuda(self):
        ayuda_screen = Screen(name='ayuda')
        ayuda_screen.add_widget(Ayuda())
        self.screen_manager.add_widget(ayuda_screen)
        
        self.screen_manager.current = 'ayuda'



class SelectColor(Screen):
    screen_manager = Organizador().screen_manager
    def set_background_color(self, color):
        color_map = {"amarillo": [1, 1, 0, 1],
                    "verde": [0, 1, 0, 1],
                    "rojo": [1, 0, 0, 1],
                    "naranja": [1, 0.5, 0, 1],
                    "morado": [0.5, 0, 1, 1],
                    "azul": [0, 0, 1, 1],
                    "cian": [0, 1, 1, 1],
                    "gris": [0.5, 0.5, 0.5, 1],
                    "blanco": [1, 1, 1, 1],
                    "negro": [0, 0, 0, 1]}
        color_rgba = color_map.get(color)
        
        self.screen_manager.canvas.add(Color(*color_rgba))
class Ayuda(Screen):
    
    def enviar(self,texto):
        
        print(texto)
    
    def borrar(self):
        self.ids.text_input.text = ''
class Musica(Screen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None
    
    def play_music(self, pista):
        if pista == 1:
            if self.sound:
                self.sound.stop()
            # Cargar el archivo de audio
            self.sound = SoundLoader.load('Assets\\Sound\\Lofi1.mp3')
        elif pista == 2:
            if self.sound:
                self.sound.stop()
            self.sound = SoundLoader.load('Assets\\Sound\\Lofi2.mp3') 
        if self.sound:
            # Establecer la propiedad loop en True para reproducir en bucle
            self.sound.loop = True
            # Reproducir el archivo de audio
            self.sound.play()   
    
    
    
    def stop_music(self):
        if self.sound:
            self.sound.stop()



class CustomScreenManager(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Reemplazar las pantallas existentes con instancias de ColorScreen modificadas
        for name, screen in self.screens.items():
            self.remove_widget(screen)
            self.add_widget(ColorScreen(name=name))
            
class ContenidoScreen(Screen):
    screen_manager = Organizador().screen_manager

    def __init__(self, contenido, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas:
            Color(0, 0, 0, 1)  # Color negro
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.contenido = contenido
        self.label = Label(text=contenido)
        self.button = Button(text="<", size_hint=(0.15, 0.05), pos_hint={"top": 0.95, "center_x": 0.17})
        self.button.bind(on_release=self.pantallaAnterior)
        self.add_widget(self.label)
        self.add_widget(self.button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def pantallaAnterior(self, *args):
        self.screen_manager.current = 'notas'
        self.screen_manager.remove_widget(self.screen_manager.get_screen('contenido'))
class PantallaMostrarNotas(Screen):
    screen_manager = Organizador().screen_manager
    notas = ListProperty([])
    def __init__(self, **kw):
        super().__init__(**kw)
        PantallaMostrarNotas.actualizar_notas(self)
    def actualizar_notas(self):
        PantallaMostrarNotas.borrar(self)
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