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
from kivy.uix.filechooser import FileChooserIconView
import base64
from PIL import Image
from io import BytesIO
import os

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')



#Aqui estoy configurando el teclado del movil
# # Window.keyboard_anim_args = {'d':.2,'t':'in_out_expo'}
# # Window.softinput_mode = "below_target"

usuarioActual = '0'

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
        # logger.debug(data.json())
        for value in data.json():
            user_reg = value['User']
            password_reg = value['Password']
            if user == user_reg:
                if password == password_reg:
                    state = True
                    self.ids.Señal_Inicio.text = 'Usuario aceptado'
                    self.screen_manager.current = 'principal'
                    id_usuario = value['id']
                else:
                    self.ids.password_input.text = '' 
                    self.ids.Señal_Inicio.text = 'Contraseña Incorrecta'
            else:
                self.ids.password_input.text = '' 
                self.ids.username_input.text = '' 
                self.ids.Señal_Inicio.text = 'Usuario Incorrecto'
        if state == True:
            usuarioActual = id_usuario
    
class Registro(Screen):
    screen_manager = Organizador().screen_manager
    
    def PantallaInicio(self,screen_manager=screen_manager):
        #Esta clase se ejecuta para cambiar de la pantalla registro a acceder, elimina los campos para que 
        #Vuelvan a quedar en blanco.

        self.ids.password_input.text = ''
        self.ids.password2_input.text = ''
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

        # logger.debug(data)
        
        if password != password2:
            state = 'No coinciden las contraseñas'
        elif len(user)<=4:
            state = 'Usuario muy corto'
        elif len(password)<=4:
            state = 'Contraseña muy corta'
        elif validate_email(email) != True:
            state = 'Email incorrecto'
        else:
            i = 0
            for value in data.json():
                i+=1
                userj= value['User']
                if userj == user:
                    state = 'El usuario exite'
                    break
            if userj != user:
                send_data = {i:{'User':user,'Password':password,'Email':email,'id':str(i),'image':"data:image/png;base64,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",'nombre_completo':'','edad':'','description':''}}
                requests.patch(url=url,json=send_data)
                state = 'Usuario registrado correctamente'
        
        self.ids.password_input.text = ''
        self.ids.password2_input.text = ''
        self.ids.email_input.text = ''
        self.ids.username_input.text = ''
        self.ids.Señal_Registro.text = state
        
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

    def imagen(self):
        imagen_screen = Screen(name='imagen')
        imagen_screen.add_widget(Imagen())
        self.screen_manager.add_widget(imagen_screen)

        self.screen_manager.current = 'imagen'
    
    def usuario(self):
        usuario_screen = Screen(name='usuario')
        usuario_screen.add_widget(Usuario())
        self.screen_manager.add_widget(usuario_screen)

        self.screen_manager.current = 'usuario'


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
class Imagen(Screen):
    url = Organizador().url
    key = Organizador().key
    data = requests.get(url + '?auth=' + key)

    def __init__(self, **kwargs):
        super(Imagen, self).__init__(**kwargs)
        for value in self.data.json():
            if usuarioActual == value['id']:
                imagen = value['image']

        self.ids.imagen.source = imagen
    
    
    def select_file(self):
        file_chooser = FileChooserIconView()

        def select_callback(*args):
            selected_file = args[1][0]  # Obtener el primer archivo seleccionado
            imagen = "data:image/png;base64," + Imagen.image_to_base64(selected_file)
            # imagen = 'Prueba'
            self.ids.imagen.source = imagen
            popup.dismiss()
            for value in self.data.json():
                if value['id'] == usuarioActual:
                    value['image'] = imagen
                    send_data = {'image': imagen}
                    url = "https://organizador-5de77-default-rtdb.europe-west1.firebasedatabase.app/" + str(value['id']) + '.json'
                    requests.patch(url=url, json=send_data)
                    break
                
        file_chooser.bind(on_submit=select_callback)

        content = Button(text="Cerrar")
        popup = Popup(title="Seleccionar imagen", content=file_chooser, size_hint=(0.9, 0.9))
        content.bind(on_release=popup.dismiss)

        popup.open()

    def image_to_base64(image_path):
        with Image.open(image_path) as image:
            # Redimensionar la imagen a un tamaño más pequeño
            resized_image = image.resize((350, 350))

            # Comprimir la imagen con una calidad específica (0-100)
            compressed_image = resized_image.copy()
            compressed_image.save("compressed_image.png", optimize=True, quality=50)

            # Convertir la imagen comprimida a base64
            buffered = BytesIO()
            compressed_image.save(buffered, format="PNG")
            encoded_string = base64.b64encode(buffered.getvalue())
            # Eliminar el archivo temporal
            os.remove("compressed_image.png")
            return encoded_string.decode("utf-8")


class Usuario(Screen):
    url = Organizador().url
    key = Organizador().key
    data = requests.get(url + '?auth=' + key)   

    def __init__(self):
        super().__init__()
        for value in self.data.json():
            if value['id'] == usuarioActual:
                self.ids.username_input.text = value['User']
                self.ids.imagen.source = value['image']
                self.ids.descripcion.text = value['description']
                self.ids.name_input.text=value['nombre_completo']


    def save(self,usuario,nombre,edad,descripcion):
        # logger.info(usuario)
        # logger.info(nombre)
        # logger.info(edad)
        # logger.info(descripcion)
        error = False
        for value in self.data.json():
            if value['id'] == usuarioActual:
                for item in self.data.json():
                    if len(usuario) < 4:
                        popup = Popup(title="Error", content=Label(text="El usuario es demasiado corto"), size_hint=(0.6, 0.6))
                        popup.open()
                        error = True
                        break
                    if usuario == item['User'] and item['id']!=usuarioActual:
                        popup = Popup(title="Error", content=Label(text="El usuario ya existe"), size_hint=(0.6, 0.6))
                        popup.open()
                        error = True
                        break


                if len(nombre) < 4:
                    popup = Popup(title="Error", content=Label(text="El nombre es demasiado corto"), size_hint=(0.6, 0.6))
                    popup.open()
                    error = True
                    break
                
                if not edad.isdigit():
                    popup = Popup(title="Error", content=Label(text="La edad debe ser un número"), size_hint=(0.6, 0.6))
                    popup.open()
                    error = True
                    break

                edad = int(edad)  # Convertir la edad a un entero

                if edad < 4 or edad >= 100:
                    popup = Popup(title="Error", content=Label(text="La edad debe estar entre 4 y 99"), size_hint=(0.6, 0.6))
                    popup.open()
                    error = True
                    break

                if len(descripcion) >= 256:
                    popup = Popup(title="Error", content=Label(text="La descripción debe tener menos de 256 caracteres"), size_hint=(0.6, 0.6))
                    popup.open()
                    error = True
                    break   
                                

                # logger.info(usuario)
                # logger.info(nombre)
                # logger.info(edad)
                # logger.info(descripcion)

                if not error:
                    send_data = {'User': usuario,'nombre_completo':nombre,'edad':str(edad),'description':descripcion}
                    url = "https://organizador-5de77-default-rtdb.europe-west1.firebasedatabase.app/" + str(value['id']) + '.json'
                    requests.patch(url=url, json=send_data)
                    break
                





# class CustomScreenManager(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Reemplazar las pantallas existentes con instancias de ColorScreen modificadas
#         for name, screen in self.screens.items():
#             self.remove_widget(screen)
#             self.add_widget(ColorScreen(name=name))
            
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




if __name__ == '__main__':
    try:
        
        Organizador().run()

    except Exception as e:
        logger.error(e)