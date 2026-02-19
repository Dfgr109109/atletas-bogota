import sys      #funcionalidad en el sistema
import os       #podemos usar funcinalidades del sistema operativo (musica e imagen)
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QWidget  
from PyQt5 import QtGui, QtCore, QtWidgets  
from PyQt5.QtGui import QPixmap #para uso de la imagen
import imagenes_rc as imagenes_rc   #para uso de la imagen
import sqlite3  #importamos la base de datos
from sqlite3 import Error   
from datetime import datetime   #fechas y tiempos
import smtplib  #envio de emails
import ssl  #garantizar la conexion segura para enviar emails
from email.message import EmailMessage  #para poder enviar correos electronicos
import winsound     #para poder reproducir la cancion

class ResultadoCarrera: #Creamos Resultado Carrera
    def __init__(self):  #encapsulamos
        self.__NoEvento=None   
        self.__NoInscripcion=None
        self.__Posicion=None
        self.__TiempoAtleta=None
        self.__IndicadorResultado=None
    def setNoEvento(self):        #Setter Numero de Evento
        self.__NoEvento = input('Ingrese número de evento:  ')     #Pedimos cada dato para luego guardarlos en la tabla Resultado carrera
    def setNoInscripcion(self):        #Setter Numero de inscripcion
        self.__NoInscripcion = input("Ingrese número de Inscripción del atleta:  ")  #Pedimos cada dato para luego guardarlos en la tabla Resultado carrera
    def setPosicion(self):        #Setter Posicion
        self.__Posicion = input("Ingrese posición final del atleta:  ")  #Pedimos cada dato para luego guardarlos en la tabla Resultado carrera
    def setTiempoAtleta(self):        #Setter Tiempo del Atleta
        self.__TiempoAtleta = input("Ingrese tiempo en que termino la carrera el atleta(HH:MM:SS):  ")  #Pedimos cada dato para luego guardarlos en la tabla Resultado carrera
    def setIndicadorResultado(self):        #Setter Indicador Resultado
        self.__IndicadorResultado = input("Ingrese indicador de resultado(R:Retiro, D:Descalificado, F:Finalizado):  ")  #Pedimos cada dato para luego guardarlos en la tabla Resultado carrera
    def setResultadoCarrera(self):  #Obtenemos el resultado Carrera para diferentes opciones de indicador de resultado
        indicador = self.__IndicadorResultado  #Volvemos la clase privada indicador de resultado como indicador
        if indicador=="F" or indicador=="f":  #Si finalizo la carrera ejecuta
            valores = (self.__NoEvento, self.__NoInscripcion, self.__Posicion, self.__TiempoAtleta, self.__IndicadorResultado)
            return valores #Envia los valores para en otra funcion poder enviarlos a la base de datos 
        elif indicador=="D":  #Si enviamos la D lo descalifica y ejecuta
            valores = (self.__NoEvento,self.__NoInscripcion,"Descalificado","Descalificado","Descalificado")  #Si indicador de resultado es D marca como descalificado
            return valores #Envia los valores para en otra funcion poder enviarlos a la base de datos 
        else: #Si se envia R retira al atleta
            valores = (self.__NoEvento,self.__NoInscripcion,"Retiro","Retiro","Retiro") 
            return valores #Envia los valores para en otra funcion poder enviarlos a la base de datos 
    def insertarResultado(self, con, valores):
        cursorObj =con.cursor()  #definir objeto cursor 
        consulta = 'INSERT INTO ResultadoCarrera (NoEvento, NoInscripcion, Posicion, TiempoAtleta, IndicadorResultado) VALUES (?, ?, ?, ?, ?)'
        cursorObj.execute(consulta, valores)    #Añadimos los datos a la tabla ResultadoCarrera
        con.commit() #Guardar persistencia
    def ModificarResultado(self, con):
        CursorObj=con.cursor()  
        Dato = input(           
    '''Seleccione el dato que desea modificar:

        1  Numero de Inscripcion
        2  Posicion 
        3  Tiempo Empleado  
        4  Indicador Novedad

        Opción seleccionada>>>: ''')   #menu de modificacion resultado
        NoInscripcion = input("Numero de Inscripcion del resultado a modificar: ") 
        if Dato == "1": #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el Numero de Inscripcion
            NoInscripcion1 = input("Nuevo Numero de Inscripcion : ")
            cadena=f'UPDATE ResultadoCarrera SET NoInscripcion = "{NoInscripcion1}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "2": #Sentencia que se ejecuta cuando el usuario selecciona la opción 2 que corresponde a cambiar la posicion
            Posicion = input("Nuevo numero de Posicion: ")
            cadena=f'UPDATE ResultadoCarrera SET Posicion = "{Posicion}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "3": #Sentencia que se ejecuta cuando el usuario selecciona la opción 3 que corresponde a cambiar el Tiempo Empleado
            TiempoAtleta = input("Nuevo Tiempo Empleado por el atleta (HH:MM:SS): ")   
            cadena=f'UPDATE ResultadoCarrera SET TiempoAtleta = "{TiempoAtleta}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "4": #Sentencia que se ejecuta cuando el usuario selecciona la opción 4 que corresponde a cambiar el Indicador Novedad
            IndicadorNovedad = input("Nueva Novedad:") 
            cadena=f'UPDATE ResultadoCarrera SET IndicadorNovedad = "{IndicadorNovedad}" WHERE NoInscripcion={NoInscripcion}'
        else: #Sentencia que se ejecuta cuando el usuario no selecciona ninguna opción valida
            print("Seleccione una opcion valida")
            self.ModificarResultado(con)
        CursorObj.execute(cadena) #Ejecuta la cadena que varia dependiendo de la elección del usuario
        con.commit()
    def mostrar_datos_ResultadoCarrera(self, con):
        NoInscripcion=input("Número de Inscripcion del atleta: ")
        cursorObj = con.cursor()
        consulta = "SELECT * FROM ResultadoCarrera ORDER BY TiempoAtleta DESC" #Buscamos loa datos de forma descendente
        cursorObj.execute(consulta)
        filas = cursorObj.fetchall()    #Recolectamos todos los datos en una lista para recorrerlos luego
        for fila in filas:
            NoEvento = fila[0]
            NoInscripcion = fila[1]
            Posicion = fila[2]
            TiempoAtleta = fila[3]
            IndicadorResultado = fila[4]
            # Obtener el nombre del atleta correspondiente al número de inscripción
        consulta_nombre_atleta = f"SELECT Nombre FROM atleta WHERE NoInscripcion = {NoInscripcion}"
        cursorObj.execute(consulta_nombre_atleta)
        nombres = cursorObj.fetchall()
        for nom in nombres:
            nombre=nom[0]
        cad = f"SELECT Apellido FROM atleta WHERE NoInscripcion = {NoInscripcion}"
        cursorObj.execute(cad)
        apellidos = cursorObj.fetchall()
        for app in apellidos:
            apellido=app[0]
            # Mostrar los datos
            print(f"No. Evento de la carrera: {NoEvento}")
            print(f"No. Inscripcion del atleta: {NoInscripcion}")
            print(f"Nombre del atleta: {nombre}")
            print(f"Apellido del atleta: {apellido}")
            print(f"Posicion del atleta: {Posicion}")
            print(f"Tiempo empleado por el atleta: {TiempoAtleta}")
            print(f"Indicador de Resultado: {IndicadorResultado}")

winsound.PlaySound("sound", winsound.SND_FILENAME)   #reproduce la cancion
def correo():   #funcion para enviar correos de confirmacion
    correoM = 'medmaratonbog@gmail.com'    #correo que usamos para enviar los mensajes
    contraseña = 'ruaeutozkwftunsj'         #contraseña del correo
    correoR = input("correo electronico (ejemplo@gmail.com): ") #correo que recive el email
    Asunto = 'Maraton de bogota'    #titulo del Email
    #contenido del email
    Contenido = """             
    Inscripcion realizada exitosamente
    """
    email = EmailMessage()  #creamos este objeto para poder crear un mensaje
    email['From'] = correoM    #correo que usamos para enviar los emails
    email['To'] = correoR       #correo que recibe los mensajes
    email['Subject'] = Asunto   #titulo del Email
    email.set_content(Contenido)    #pasamos el contenido del email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:  #servidor SMTP y numero de puerto para poder enviar los emails 
        smtp.login(correoM, contraseña)         #ingresamos el usuario y contraseña para ingresar al correo que envia emails
        smtp.sendmail(correoM, correoR, email.as_string())  #Enviamos el email al correo dado

class ClasificacionFinal(ResultadoCarrera):#Definimos la clase
    def __init__(self): #iniciamos a definir las propiedades y encapsular
        self.__NoEvento=None   
        self.__NoInscipcion=None
        self.__Nombre=None
        self.__Apellido=None
        self.__FechaNacimiento=None
        self.__PaisOrigen=None
        self.__CiudadOrigen=None
        self.__TiempoAtleta=None
    def setNoInscripcion(self): #definimos metodo set para obtener el NoInscripcion
        self.__NoInscripcion = input("Número de inscripción del atleta a consultar: ")  #pedimos el numero que nos va a guardar en NoInscripcion
        return self.__NoInscripcion #Mandamos el numero cualquiera que llame el metodo
    
    class Ui_Menu(object):  #Clase de PyQt que se encarga de la ventana del Menu de la grafica

        def closeWindow(self):  #cierra la ventana
            sys.exit()  #Cierra la ventana

        def returnToTerminal(self): #Hacemos que vuelva a la terminal
            QtWidgets.qApp.closeAllWindows()    
            script_path = os.path.abspath(sys.argv[0])  
            python_executable = sys.executable
            process = QtCore.QProcess()
            process.startDetached(python_executable, [script_path])

        def setupUi(self, Menu):   #Propiedades y objetos de la ventana menu
            Menu.setObjectName("Menu")      #Definimos nombre del objeto
            Menu.setWindowModality(QtCore.Qt.NonModal)      
            Menu.setEnabled(True)
            Menu.resize(900, 600)  #Tamaño de la pagina
            font = QtGui.QFont()  #Para ediciones de la letra
            font.setFamily("MS Reference Sans Serif")  #Tipo de letra
            font.setPointSize(7)  #Tamaño de letra
            Menu.setFont(font)
            Menu.setFocusPolicy(QtCore.Qt.NoFocus)
            Menu.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
            Menu.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)   
            self.centralwidget = QtWidgets.QWidget(Menu)
            self.centralwidget.setObjectName("centralwidget")
            self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=Menu.close) #hacemos que el boton cierre la ventana
            self.pushButton.setGeometry(QtCore.QRect(280, 240, 401, 61))    #Posicion del boton
            font = QtGui.QFont()    
            font.setFamily("MS Reference Sans Serif")   #tipo de letra
            font.setPointSize(12)
            self.pushButton.setFont(font)
            self.pushButton.setObjectName("pushButton")  #Creamos un botom
            self.label = QtWidgets.QLabel(self.centralwidget)   #El titulo menu
            self.label.setGeometry(QtCore.QRect(280, 30, 401, 51))  #geometria del cuadro de titulo
            font = QtGui.QFont()
            font.setFamily("MS Reference Sans Serif")   #tipo de letra
            font.setPointSize(26)  #Tamaño de letra
            self.label.setFont(font)    
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("label")      
            self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)   #definimos el boton 2
            self.pushButton_2.setGeometry(QtCore.QRect(280, 360, 401, 61))  #geometria del boton
            self.pushButton_2.clicked.connect(self.returnToTerminal)    #hacemos que el click del boton nos devuelva a la terminal
            
            font = QtGui.QFont()  #para editar propiedades del texto
            font.setFamily("MS Reference Sans Serif")   #tipo de letra
            font.setPointSize(12)  #Tamaño letra
            self.pushButton_2.setFont(font)  
            self.pushButton_2.setObjectName("pushButton_2") #Creamos un segundo boton
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(740, 10, 151, 111))   #geometria del boton 2
            font = QtGui.QFont()  #Para editar letra 
            font.setFamily("MS Reference Sans Serif") #Tipo de letra
            font.setPointSize(5)  
            self.label_2.setFont(font)
            self.label_2.setText("")
            self.label_2.setObjectName("label_2")    #nombre del cuadro de texto
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            Menu.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(Menu) 
            self.statusbar.setObjectName("statusbar")   #nombre del statusbar
            Menu.setStatusBar(self.statusbar)   
            self.retranslateUi(Menu)
            QtCore.QMetaObject.connectSlotsByName(Menu) 
            Menu.setTabOrder(self.pushButton, self.pushButton_2)    #orden de botones
            # Acceder al recurso empaquetado
            pixmap = QPixmap(":/logo.png") #Accedemos a la imagen donde esta guardada
            self.label_2.setPixmap(pixmap)  #Volvemos map de bits la imagen
        def retranslateUi(self, Menu):  #Propiedades ventana menu
            _translate = QtCore.QCoreApplication.translate
            Menu.setWindowTitle(_translate("Menu", "Atletismo Bogota")) #titulo de la ventana
            self.pushButton.setText(_translate("Menu", "Consultar"))  #Titulo Boton 1 de consultar
            self.label.setText(_translate("Menu", "Menú")) #label donde dice menu
            self.pushButton_2.setText(_translate("Menu", "Salir"))  #Boton 2 de salir
            
    class Ui_ConsultaWindow(object):  #Creamos la ventana de consulta
        def setupUi(self, ConsultaWindow):  #Ventana de consulta
            ConsultaWindow.setObjectName("ConsultaWindow")  #nombre de la ventana
            ConsultaWindow.resize(900, 600) #dimensiones de la ventana
            self.centralwidget = QtWidgets.QWidget(ConsultaWindow)
            self.centralwidget.setObjectName("centralwidget")

            font = QtGui.QFont() #Para editar letra
            font.setPointSize(12)
            self.label = QtWidgets.QLabel(self.centralwidget)   
            self.label.setGeometry(QtCore.QRect(270, 20, 350, 100)) #geometria del cuadro de texto
            font = QtGui.QFont()    
            font.setPointSize(26)   #tamaño
            self.label.setFont(font)    
            self.label.setObjectName("label") #nombre del cuadro de texto

            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(740, 10, 151, 111)) #geometria de label 2
            font = QtGui.QFont() #para editar la letra
            font.setFamily("MS Reference Sans Serif")   #tipo de letra
            font.setPointSize(5)
            self.label_2.setFont(font)
            self.label_2.setText("")
            self.label_2.setObjectName("label_2")   #nombre del cuadro de texto
            self.label_2 = QtWidgets.QLabel(self.centralwidget)

            self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
            self.tableWidget.setGeometry(QtCore.QRect(25, 200, 780, 190))   #dimensiones y posicion de la tabla
            self.tableWidget.setRowCount(6) #numero de filas
            self.tableWidget.setColumnCount(8)  #numero de columnas
            self.tableWidget.setObjectName("tableWidget")   #nombre de la tabla
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) #prohibimos al usuario modificar la informacion dada en la tabla

            self.ExitButtom = QtWidgets.QPushButton(self.centralwidget)   #definimos el boton 2
            self.ExitButtom.setGeometry(QtCore.QRect(300, 450, 211, 31))  #geometria del boton
            self.ExitButtom.clicked.connect(self.returnToTerminal)    #hacemos que el click del boton nos devuelva a la terminal

            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)   #columna numero 0
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)   #columna numero 1
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(2, item)      #columna numero 2
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(3, item)   #columna numero 3
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(4, item)   #columna numero 4
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(5, item) #columna numero 5
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(6, item)   #columna numero 6
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(7, item) #columna numero 7
            ConsultaWindow.setCentralWidget(self.centralwidget)
            self.tableWidget.setSortingEnabled(True)            #ordena por columna como pida el usuario
            self.menubar = QtWidgets.QMenuBar(ConsultaWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
            self.menubar.setObjectName("menubar")   #nombre del menubar
            ConsultaWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(ConsultaWindow)
            self.statusbar.setObjectName("statusbar")   #nombre del statusbar
            ConsultaWindow.setStatusBar(self.statusbar)

            self.retranslateUi(ConsultaWindow) #pasamos las propiedades de la ventana a retranslateUi para asignarles un titulo
            QtCore.QMetaObject.connectSlotsByName(ConsultaWindow)

            # Acceder al recurso empaquetado
            pixmap = QPixmap(":/logo.png")  #Accedemos al Logo del programa
            self.label_2.setPixmap(pixmap)  #Convertimos image a png

        def retranslateUi(self, ConsultaWindow):    #asignamos texto a cada elemento de la ventana
            _translate = QtCore.QCoreApplication.translate
            ConsultaWindow.setWindowTitle(_translate("ConsultaWindow", "MainWindow"))   #titulo de la respectiva columna
            self.label.setText(_translate("ConsultaWindow", "Clasificación final")) #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(0) 
            item.setText(_translate("ConsultaWindow", "NoEvento"))  #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(1) 
            item.setText(_translate("ConsultaWindow", "NoInscripcion")) #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(2) 
            item.setText(_translate("ConsultaWindow", "Nombre"))    #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(3) 
            item.setText(_translate("ConsultaWindow", "Apellido"))  #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(4) 
            item.setText(_translate("ConsultaWindow", "FechaNacimiento"))   #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(5) 
            item.setText(_translate("ConsultaWindow", "PaisOrigen"))    #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(6) 
            item.setText(_translate("ConsultaWindow", "CiudadOrigen"))  #titulo de la respectiva columna
            item = self.tableWidget.horizontalHeaderItem(7) 
            item.setText(_translate("ConsultaWindow", "TiempoAtleta"))  #titulo de la respectiva columna
            self.ExitButtom.setText(_translate("Menu", "Salir"))        #titulo del boton
            
        def returnToTerminal(self): #hacemos que vuelva a la terminal
            QtWidgets.qApp.closeAllWindows()    #cierra la ventana
            script_path = os.path.abspath(sys.argv[0])  
            python_executable = sys.executable
            process = QtCore.QProcess()
            process.startDetached(python_executable, [script_path])   #ejecuta el codigo

        def mostrar_datos(self):
            # Conexión a la base de datos SQLite
            con = sqlite3.connect('Nueva.db')  # Conecta a la base de datos SQLite llamada 'Nueva.db'
            cursor = con.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
            cad = self.obtener_cadena_consulta()  # Obtener la cadena de consulta
            cursor.execute(cad)  # Ejecuta la consulta SQL en la base de datos
            datos = cursor.fetchall()  # Obtiene todos los resultados de la consulta
            print(datos)  # Imprime los datos obtenidos
            # Establecer el número de filas y columnas de la tabla
            self.tableWidget.setRowCount(len(datos))  # Establece el número de filas de la tabla según la cantidad de datos
            self.tableWidget.setColumnCount(len(datos[0]))  # Establece el número de columnas de la tabla según la cantidad de datos en la primera fila
            # Insertar los datos en la tabla
            for i, fila in enumerate(datos):  # Recorre cada fila de datos
                for j, dato in enumerate(fila):  # Recorre cada dato de la fila
                    item = QTableWidgetItem(str(dato))  # Crea un QTableWidgetItem con el dato convertido a cadena
                    self.tableWidget.setItem(i, j, item)  # Inserta el QTableWidgetItem en la posición correspondiente de la tabla
    
        def obtener_cadena_consulta(self):
            print('''Seleccione el dato por el que desea ordenar:
            
            1  Numero de Inscripcion
            2  Tiempo Empleado
            3  Nombre
            4  Apellido
            5  FechaNacimiento
            6  PaisOrigen
            7  CiudadOrigen
            ''')
            opcion = input('''¿Porque campo desea ordenar?
                        ''') # Ordena lista por defecto
            if opcion == "1":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY NoInscripcion ASC"  # Consulta SQL para ordenar por número de inscripción ascendente
            elif opcion == "2":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY TiempoAtleta ASC"  # Consulta SQL para ordenar por tiempo de atleta ascendente
            elif opcion == "3":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY Nombre ASC"  # Consulta SQL para ordenar por nombre ascendente
            elif opcion == "4":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY Apellido ASC"  # Consulta SQL para ordenar por apellido ascendente
            elif opcion == "5":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY FechaNacimiento ASC"  # Consulta SQL para ordenar por fecha de nacimiento ascendente
            elif opcion == "6":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY PaisOrigen ASC"  # Consulta SQL para ordenar por país de origen ascendente
            elif opcion == "7":
                cad = "SELECT * FROM ClasificacionFinal ORDER BY CiudadOrigen ASC"  # Consulta SQL para ordenar por ciudad de origen ascendente
            else:
                cad = "SELECT * FROM ClasificacionFinal"  # Opción por defecto: consulta SQL sin ordenamiento
            return cad  # Retorna la cadena de consulta SQL
class Carrera:
    def __init__(self):
        self.__NoEvento=None   
        self.__Year=None
        self.__PremioPrimerP=None
        self.__PremioSegundoP=None
        self.__PremioTercerP=None
    def setNoEvento(self): #se leen los datos para luego registrarlos en una tabla usando otra funcion
        self.__NoEvento=input("Numero de evento: ")
    def setYear(self):
        self.__Year=input("Año(YYYY): ")
        self.__Año=datetime.strptime(self.__Year,"%Y").date() #datetime para la variable que contiene una fecha
        self.__Año = int(self.__Año.strftime("%Y"))  
    def setPremioPrimerP(self):
        self.__PremioPrimerP=input("Premio primer puesto: ")
        self.__PremioPrimerP=self.__PremioPrimerP.ljust(12)   #usamos ljust para correr el texto a la izquierda
    def setPremioSegundoP(self):
        self.__PremioSegundoP=input("Premio segundo puesto: ")
        self.__PremioSegundoP=self.__PremioSegundoP.ljust(12)
    def setPremioTercerP(self):
        self.__PremioTercerP=input("Premio tercer puesto: ")
        self.__PremioTercerP=self.__PremioTercerP.ljust(12)
    def setCarrera(self):
        carrera=(self.__NoEvento, self.__Año, self.__PremioPrimerP, self.__PremioSegundoP, self.__PremioTercerP)
        return carrera
    def insertar_tabla_carrera(self, con, carrera):
        cursorObj =con.cursor()
        cadena='INSERT INTO carrera VALUES (?,?,?,?,?)'#Registramos los datos en una tabla, estos fueron leidos en otra funcion
        cursorObj.execute(cadena, carrera)
        con.commit()
    def borrarInfoCarrera(self, con):
        CursorObj=con.cursor()
        buscar = input("Numero de evento que desea borrar: ")
        cadena=f'DELETE FROM carrera WHERE NoEvento={buscar}' # borramos de la tabla carrera donde el nomero de evento sea
        CursorObj.execute(cadena)                                   #la variable que pedimos antes
        con.commit()
    def consultarCarrera(self, con):
        CursorObj=con.cursor()
        NoEvento=input("Número de evento a consultar: ") 
        cad=f'SELECT * FROM carrera WHERE NoEvento={NoEvento}' #Buscamos los datos en la tabla donde aparece el numero de evento
        print(NoEvento)
        CursorObj.execute(cad)  
        filas=CursorObj.fetchall()  #Recolectamos todos los datos en una lista para poder recorrerlos
        for fila in filas:             #recorremos la lista para mostrar los datos
            NoEvento = fila[0]   
            Año = fila[1] 
            PremioPP = fila[2]  
            PremioSP = fila[3]  
            PremioTP = fila[4]  
            print("El numero de evento es: ", NoEvento) 
            print("El año de la carrera es: ", Año)
            print("El premio del primer puesto es: ", PremioPP)
            print("El premio del segundo puesto es: ", PremioSP)
            print("La premio del tercer puesto es: ", PremioTP)
    def actualizarCarrera(self, con):  #Creamos función de actualizar atleta
        CursorObj=con.cursor()  
        Dato = input('''
    Seleccione el dato que desea modificar:

    1  Año
    2  Premio primer puesto  
    3  Premio segundo puesto
    4  Premio tercer puesto

    Opción seleccionada>>>: ''')   #Se hace un menu para modificar especialmente un dato que guardaremos en esta variable
        NoEvento = input("Numero evento a modificar: ")  #Se pide el número de evento que se quiere modificar
        if Dato == "1":     #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el Año
            Year=input("Ingrese un nuevo año de carrera: ")
            Año=datetime.strptime(Year,"%Y").date()
            Año = int(Año.strftime("%Y"))
            cadena=f'UPDATE carrera SET Año = "{Año}" WHERE NoEvento={NoEvento}'
        elif Dato == "2":   #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el premio primer puesto
            PremioPP = input("Nuevo premio de primer puesto: ")
            cadena=f'UPDATE carrera SET PremioPrimerP = "{PremioPP}" WHERE NoEvento={NoEvento}'
        elif Dato == "3":   #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el premio segundo puesto
            PremioSP = input("Nuevo premio de segundo puesto : ")
            cadena=f'UPDATE carrera SET PremioSegundoP = "{PremioSP}" WHERE NoEvento={NoEvento}'
        elif Dato == "4":   #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el premio tercer puesto
            PremioTP = input("Nuevo premio para segundo puesto: ") 
            cadena=f'UPDATE carrera SET PremioTercerP = "{PremioTP}" WHERE NoEvento={NoEvento}'
        else:   # Al digitar un numero que no corresponda con las opciones del menú volvemos a llamar
            print("Seleccione una opcion valida")   #la funcion hasta que se digite un numero valido
            self.actualizarCarrera(con)
        CursorObj.execute(cadena) 
        con.commit()
class Atleta:
    def __init__(self):
        self.__NoIdAtleta=None   
        self.__NoInscripcion=None
        self.__Nombre=None
        self.__Apellido=None
        self.__FechaNacimiento=None
        self.__PaisOrigen=None
        self.__CiudadOrigen=None
    def setNoIdAtleta(self):
        self.__NoIdAtleta=input("Identificacion del atleta: ")  #Entrada de Número de Identificación del atleta
        self.__NoIdAtleta=self.__NoIdAtleta.ljust(12)  #Todos los ljust son para alinear el texto a la izquierda
    def setNoInscripcion(self):
        self.__NoInscripcion=input("Numero de Inscripcion del atleta:")   #Entrada de Número de Inscripción del atleta
        self.__NoInscripcion=self.__NoInscripcion.ljust(12)
    def setNombre(self):
        self.__Nombre=input("Nombre del atleta: ").upper()  #Entrada del nombre del atleta 
        self.__Nombre=self.__Nombre.ljust(12)
    def setApellido(self):
        self.__Apellido=input("Apellido del atleta: ").upper()  #Entrada del apellido del atleta
        self.__Apellido=self.__Apellido.ljust(12)
    def setFechaNacimiento(self):
        FechaNacimientoEntrada=input("Fecha de nacimiento (AAAA-MM-DD): ")  #Entrada de fecha de nacimiento del atleta
        self.__FechaNacimiento=datetime.strptime(FechaNacimientoEntrada,'%Y-%m-%d').date() #El date es para quitar segundos, minutos, horas
    def setPaisOrigen(self):
        self.__PaisOrigen=input("Pais de origen del atleta: ").upper()  #Entrada del pais de origen del atleta
        self.__PaisOrigen=self.__PaisOrigen.ljust(12)
    def setCiudadOrigen(self):
        self.__CiudadOrigen=input("Ciudad de origen del atleta: ").upper() #Entrada de la Ciudad de Origen del atleta
        self.__CiudadOrigen=self.__CiudadOrigen.ljust(12)
    def setatleta(self):
        atleta=(self.__NoIdAtleta, self.__NoInscripcion, self.__Nombre, self.__Apellido, self.__FechaNacimiento, self.__PaisOrigen, self.__CiudadOrigen) #Guardar información del atleta 
        return atleta
    def insertar_atleta(self, con, atleta): #Inserta los valores guardados en atleta en la tabla 
        cursorObj =con.cursor()
        cadena='INSERT INTO atleta VALUES (?,?,?,?,?,?,?)'  #Cadena de sql para insertar un atleta, los ? se remplazan por los valores traidos de la informacion guardada en atleta
        cursorObj.execute(cadena, atleta) #Ejecutar cadena con valores de atleta                  
        con.commit()
    def consultar_atleta(self, con):  #consultar Los datos del atleta
        CursorObj=con.cursor()
        NoInscripcion=input("Número de inscripción del atleta a consultar: ")  #Se recibe el número de inscripción del atleta que se va a consultar
        cad=f'SELECT * FROM atleta WHERE NoInscripcion={NoInscripcion}'  #Cadena ejecutable de sql
        CursorObj.execute(cad)  #Se ejecuta la cadena
        filas=CursorObj.fetchall()  #Se separan las filas de la columna 
        for fila in filas:  #Se crea un iterable en filas para iterar en cada fila y asi obtener la informacion por partes
            NoIdAtleta = fila[0]  #Se trae la primera información de la lista filas que corresponde a NoIdAtleta
            NoInscripcion = fila[1]  #Se trae la segunda información de la lista filas que corresponde a NoInscripción
            Nombre = fila[2]  #Se trae la tercera información de la lista filas que corresponde a Nombre
            Apellido = fila[3]  #Se trae la cuarta información de la lista filas que corresponde a Apellido
            FechaNacimiento = fila[4]  #Se trae la quinta información de la lista filas que corresponde a Fecha de nacimiento
            PaisNacimiento = fila[5]  #Se trae la sexta información de la lista filas que corresponde a Pais de nacimiento
            CiudadNacimiento = fila[6]  #Se trae la septima información de la lista filas que corresponde a Ciudad de nacimiento
            print("La identificacion del atleta es: ", NoIdAtleta) #Se imprimen los valores hallados
            print("El número de inscripcion del atleta es: ", NoInscripcion)
            print("El nombre del atleta es: ", Nombre)
            print("El apellido del atleta es: ", Apellido)
            print("La fecha de nacimiento del atleta es: ", FechaNacimiento)
            print("El pais de nacimiento del atleta es: ", PaisNacimiento)
            print("La ciudad de nacimiento del atleta es: ", CiudadNacimiento)
    def actualizar_atleta(self, con):  #Creamos función de actualizar atleta
        CursorObj=con.cursor()  
        Dato = input(
    '''Seleccione el dato que desea modificar:
        
        1  Nombre del atleta 
        2  Apellido del atleta
        3  Numero de identificación del atleta  
        4  Fecha de nacimiento del atleta  
        5  Pais de origen del atleta 
        6  Ciudad de origen del atleta

        Opción seleccionada>>>: ''')  #Se hace un menu para modificar especialmente un dato que guardaremos en esta variable 
        NoInscripcion = input("NoInscripcion del atleta a modificar: ")  #Se pide el número de inscripción del atleta que se quiere modificar
        if Dato == "1": #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a cambiar el nombre
            Nombre = input("Nuevo nombre: ").upper() #Se pide el nuevo nombre
            cadena=f'UPDATE atleta SET Nombre = "{Nombre}" WHERE NoInscripcion={NoInscripcion}' #Sentencia que se ejecutara en sqlite
        elif Dato == "2": #Sentencia que se ejecuta cuando el usuario selecciona la opción 2 que corresponde a cambiar el apellido
            Apellido = input("Nuevo apellido : ").upper()
            cadena=f'UPDATE atleta SET Apellido = "{Apellido}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "3": #Sentencia que se ejecuta cuando el usuario selecciona la opción 3 que corresponde a cambiar el Número de id del atleta
            NoIdAtleta = input("Nuevo numero de identificación del atleta: ")
            cadena=f'UPDATE atleta SET NoIdAtleta = "{NoIdAtleta}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "4": #Sentencia que se ejecuta cuando el usuario selecciona la opción 4 que corresponde a cambiar la fecha de nacimiento
            FechaNacimiento1 = input("Nueva Fecha de nacimiento (AAAA-MM-DD) del atleta: ")
            FechaNacimiento=datetime.strptime(FechaNacimiento1,'%Y-%m-%d').date()
            cadena=f'UPDATE atleta SET FechaNacimiento = "{FechaNacimiento}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "5": #Sentencia que se ejecuta cuando el usuario selecciona la opción 5 que corresponde a cambiar el pais de origen
            PaisOrigen = input("Nuevo Pais de Origen del atleta:") 
            cadena=f'UPDATE atleta SET PaisOrigen = "{PaisOrigen}" WHERE NoInscripcion={NoInscripcion}'
        elif Dato == "6": #Sentencia que se ejecuta cuando el usuario selecciona la opción 6 que corresponde a cambiar la ciudad de origen
            CiudadOrigen = input("Nueva Ciudad de Origen del atleta:")
            cadena=f'UPDATE atleta SET CiudadOrigen = "{CiudadOrigen}" WHERE NoInscripcion={NoInscripcion}'
        else: #Sentencia que se ejecuta cuando el usuario no selecciona ninguna opción valida
            print("Seleccione una opcion valida")
            self.actualizar_atleta(con) #Vuelve a ejecutar la función hasta que el usuario tenga una opción valida
        CursorObj.execute(cadena) #Ejecuta la cadena que varia dependiendo de la elección del usuario
        con.commit()
    def borrar_info_atleta(self, con):  #Se hace para borrar un atleta
        CursorObj=con.cursor()
        Dato = input(
    '''Que dato desea usar como referencia para borrar el atleta:
        
        1  Numero de inscripción del atleta
        2  Numero de identificación del atleta  

        Opción seleccionada>>>: ''')  #Se hace un menu para borrar atleta con número de identificación o número de inscripción lo guardaremos en esta variable 
        if Dato == "1": #Sentencia que se ejecuta cuando el usuario selecciona la opción 1 que corresponde a borrar con número de inscripción del atleta
            NoInscripción = input("Ingrese el numero de inscripción del atleta a borrar: ") #Se pide el número de inscripción del atleta que se va a borrar
            cadena=f'DELETE FROM atleta WHERE NoInscripcion={NoInscripción}' #Sentencia que se ejecutara en sqlite
        elif Dato == "2": #Sentencia que se ejecuta cuando el usuario selecciona la opción 2 que corresponde a borrar con número de identificación del atleta
            NoIdAtleta = input("Ingrese el número de identificación del atleta a borrar: ")  #Se pide el número de identificación del atleta que se va a borrar y lo guardaremos en esta variable 
            cadena=f'DELETE FROM atleta WHERE NoIdAtleta LIKE "{NoIdAtleta}%"'
        else: #Sentencia que se ejecuta cuando el usuario no selecciona ninguna opción valida
            print("Seleccione una opción correcta  ")
            self.borrar_info_atleta(con) #Se vuelve a ejecutar hasta elegir una opción correcta
        CursorObj.execute(cadena)  #Se ejecuta cadena de sql
        con.commit()
def conexion_db():  #Crea Base de datos y conexion con la base de datos 
    try:
        con = sqlite3.connect('Nueva.db')
        return con
    except Error:
        print(Error)
def autenticar_usuario(): #Creamos esta función para poder darle opciones especiales al administrador
    usuario = input("Ingrese su nombre de usuario: ") #Aqui recibimos el nombre de usuario para luego poder verificar si es o no administrador
    contrasena = input("Ingrese su contraseña: ")  #Aqui recibimos la clave del usuario para luego poder verificar si es o no administrador
    administradores = {"Profesor":"POO123","Daniel": "1234", "Jose":"4321", "Grimaldo":"1234", "Harold":"Monitor"} #Lista de administradores {usuario:clave}
    EsAdmin = False #Variable que parte de que nadie es administrador
    for c in administradores: #Iterador en administradores
        if usuario == c and contrasena==administradores.get(c): #Verifica si el usuario es administrador
            EsAdmin = True  #Si es administrador cambia la variable a verdadero
    return EsAdmin #retorna si es administrador o no para dar las opciones de cada rol
def crear_tabla_atleta(con):  #Creamos tabla atleta 
    cursorObj =con.cursor()  #Se crea objeto cursor con el que podremos hacer una consulta en sql
    cadena='''CREATE TABLE IF NOT EXISTS atleta(    
                NoIdAtleta TEXT NOT NULL,
                NoInscripcion INTEGER NOT NULL,
                Nombre TEXT,
                Apellido TEXT,
                FechaNacimiento DATE, 
                PaisOrigen TEXT,
                CiudadOrigen TEXT,
                PRIMARY KEY (NoIdAtleta, NoInscripcion))'''
    cursorObj.execute(cadena)  #Ejecutar cadena de comandos sql
    con.commit()  #Guardar persistencia en el disco
def crear_tabla_ClasificacionFinal(con):
    cursorObj = con.cursor()    #Recorremos la BD con el objeto de conexion
    cadena = '''CREATE TABLE IF NOT EXISTS ClasificacionFinal(
                NoEvento TEXT NOT NULL,
                NoInscripcion INTEGER NOT NULL,
                Nombre TEXT,
                Apellido TEXT,
                FechaNacimiento DATE,
                PaisOrigen TEXT,
                CiudadOrigen TEXT,
                TiempoAtleta TEXT,
                FOREIGN KEY (NoEvento) REFERENCES carrera (NoEvento),
                FOREIGN KEY (NoInscripcion) REFERENCES atleta (NoInscripcion)
                )'''
    cursorObj.execute(cadena) #Creamos la tabla, usamos el FOREING KEY refiriendonos al PRIMARY KEY las tablas carrera
    con.commit()                # y atleta para así recolectar los datos del campo especificado, en este caso NoEvento y NoInscripcion
def CrearTablaCarrera(con):
    cursorObj =con.cursor() #Recorremos la BD con el objeto de conexion
    cadena='''CREATE TABLE IF NOT EXISTS carrera(
                NoEvento INTEGER NOT NULL,
                Año INTEGER NOT NULL,
                PremioPrimerP TEXT,
                PremioSegundoP TEXT,
                PremioTercerP TEXT, 
                PRIMARY KEY (NoEvento))'''
    cursorObj.execute(cadena) #Creamos la tabla
    con.commit()
def CrearTablaResultadoCarrera(con):
    cursorObj = con.cursor()   #Recorremos la BD con el objeto de conexion
    cadena = '''CREATE TABLE IF NOT EXISTS ResultadoCarrera(
                NoEvento INTEGER NOT NULL,
                NoInscripcion INTEGER NOT NULL,
                Posicion INTEGER NOT NULL,
                TiempoAtleta DATE,
                IndicadorResultado TEXT, 
                FOREIGN KEY (NoEvento) REFERENCES carrera (NoEvento),       
                FOREIGN KEY (NoInscripcion) REFERENCES atleta (NoInscripcion)
                )'''
    cursorObj.execute(cadena)   #Creamos la tabla, usamos el FOREING KEY refiriendonos al PRIMARY KEY las tablas carrera
    con.commit()                 # y atleta para así recolectar los datos del campo especificado, en este caso NoEvento y NoInscripcion
def borrar_tabla(con):  #Se crea función para borrar una tabla 
    CursorObj=con.cursor()
    Nombre=input("Nombre de tabla a borrar: ") #Definimos nombre para pasar el nombre de la tabla a borrar
    cadena=f'DROP TABLE {Nombre}' #Cadena ejecutable sqlite
    CursorObj.execute(cadena) #Ejecutamos cadena
    con.commit()    #Guardamos lo que hacemos
def menu_usuario(conex, objetoCarrera, ObjetoAtleta, objetoResultadoCarrera, objetoClasificacion):#Definimos el menu que le saldra al usuario 
    salirPrincipal=False  #Hacemos una bandera para guardar booleano
    while not salirPrincipal:  #Definimos un ciclo mientras no se cumpla la bandera
        opcPrincipal=input('''
Menu Principal
1  Administración de Carreras
2  Administración de Atletas
3  Administración de Resultados de Carrera
4  Consulta de la Clasificación Final
5  Salir
Opción seleccionada>>>: ''') #Este sera el menu de opciones a elegir
        if (opcPrincipal=='1'):  #Condicional al elegir 1
            salirCarrera=False
            while not salirCarrera:  #Ciclo mientras no salga del menu de carreras
                opcCarrera=input('''
Menú Administración de Carreras
1  Crear una Carrera en la Base de Datos
2  Modificar información de una Carrera
3  Consultar información de una Carrera
4  Salir
Opción seleccionada>>>:  ''')
                if (opcCarrera=='1'):  #Condicional al elegir el 1
                    datos=objetoCarrera.IngresarDatosCarrera()
                    objetoCarrera.insertar_tabla_carrera(conex, datos)
                elif (opcCarrera=='2'):
                    objetoCarrera.actualizarCarrera(conex)
                elif (opcCarrera=='3'):
                    objetoCarrera.consultarCarrera(conex)
                elif (opcCarrera=='4'):
                    salirCarrera=True
        elif (opcPrincipal=='2'):    #Condicional al elegir 2
            salirAtletas=False
            while not salirAtletas:  #Ciclo que sucedera mientras no salgamos de administrar atletas
                opcAtletas=input('''
Menú Administración de Atletas
1  Crear un Atleta en la Base de Datos
2  Modificar información de un Atleta
3  Consultar información de un Atleta
4  Salir
Opción seleccionada>>>:  ''')  #Menu de administración de atletas
                if (opcAtletas=='1'):  #Condicional para opción 1
                    ObjetoAtleta.setNoIdAtleta()
                    ObjetoAtleta.setNoInscripcion()
                    ObjetoAtleta.setNombre()
                    ObjetoAtleta.setApellido()
                    ObjetoAtleta.setFechaNacimiento()
                    ObjetoAtleta.setPaisOrigen()
                    ObjetoAtleta.setCiudadOrigen()
                    atletacreado=ObjetoAtleta.setatleta()
                    ObjetoAtleta.insertar_atleta(conex, atletacreado)
                    pregunta = input("¿Desea que le enviemos un correo electronico confirmando su inscripcion?(si/no): ")
                    if (pregunta == "si"):
                        correo()
                elif (opcAtletas=='2'):  #Condicional para opción 2
                    ObjetoAtleta.actualizar_atleta(conex) 
                elif (opcAtletas=='3'):  #Condicional para opción 3
                    ObjetoAtleta.consultar_atleta(conex)
                elif (opcAtletas=='4'):  #Condicional para opción 4
                    salirAtletas=True
        elif (opcPrincipal=='3'): #Condicional para opción 3 del menu principal
            salirResultado=False
            while not salirResultado:  #Ciclo mientras no se salga del menu de resultados de carrera
                opcResultado=input('''
Menú de administración Resultado 
1  Ver resultado carrera
2  Salir
Opción seleccionada>>>:  ''')
                if (opcResultado=='1'):  #Condicional para opción 1
                    objetoResultadoCarrera.mostrar_datos_ResultadoCarrera(conex)
                elif (opcResultado=='2'):
                    salirResultado=True
        elif (opcPrincipal=='4'): #Condicional para opción 4 del menu principal
            salirConsulta=False
            while not salirConsulta:  #Ciclo que sucedera mientras no salgamos de Consulta clasificación final
                opcConsulta=input('''
Menú de Consulta de la Clasificación Final 
1  Consultar Clasificación general
2  Salir
Opción seleccionada>>>:  ''')  #Menú de Clasificación final
                if (opcConsulta=='1'):  #Condicional para opción 1
                    
                    app = QApplication(sys.argv)    
                    MainWindow = QMainWindow()  #ventana del Menu
                    u = objetoClasificacion.Ui_Menu()   
                    u.setupUi(MainWindow)
                    MainWindow.show()   #aparece la ventana en la pantalla
                    app.exec_()     #procesa la ventana

                    Window2 = QMainWindow() #ventana de la consulta
                    Ui2 = objetoClasificacion.Ui_ConsultaWindow()
                    Ui2.setupUi(Window2)
                    #Window2.exit_button.clicked.connect(Window2.close)
                    Ui2.mostrar_datos() #llamamos al metodo para mostrar datos en la tabla
                    Window2.show()  #aparece la ventana de consulta en la pantalla
                    app.exec_()     #procesa la ventana (botones, informacion ingresada, etc)

                elif (opcConsulta=='2'):
                    salirConsulta=True
        elif (opcPrincipal=='5'): #Condicional para opción 5 del menu principal
            salirPrincipal=True
    print('Programa finalizado.  Gracias por utilizar nuestros servicios.') #Mensaje al salir de ambos menus
def menu_administrador(conex, objetoCarrera, ObjetoAtleta, objetoResultadoCarrera, objetoClasificacion): #Definimos el menu que le saldra al administrador
    salirPrincipal=False
    while not salirPrincipal:  #Ciclo mientras no salga del menu principal
        opcPrincipal=input('''
Menu Principal
1  Administración de Carreras
2  Administración de Atletas
3  Administración de Resultados de Carrera
4  Consulta de la Clasificación General
5  Salir
Opción seleccionada>>>: ''') #Opciones del menu principal
        if (opcPrincipal=='1'):  #Condicional al elegir el 1
            salirCarrera=False
            while not salirCarrera:  #Ciclo mientras no salga del menu de carreras
                opcCarrera=input('''
Menú Administración de Carreras
1  Crear una Carrera en la Base de Datos
2  Modificar información de una Carrera
3  Consultar información de una Carrera
4  Borrar información de una Carrera
5  Borrar tabla de Carrera
6  Salir
Opción seleccionada>>>:  ''')
                if (opcCarrera=='1'):  #Condicional al elegir el 1
                    #datos=objetoCarrera.IngresarDatosCarrera()
                    objetoCarrera.setNoEvento()
                    objetoCarrera.setYear()
                    objetoCarrera.setPremioPrimerP()
                    objetoCarrera.setPremioSegundoP()
                    objetoCarrera.setPremioTercerP()
                    carreraCreada= objetoCarrera.setCarrera()
                    objetoCarrera.insertar_tabla_carrera(conex, carreraCreada)
                elif (opcCarrera=='2'):
                    objetoCarrera.actualizarCarrera(conex)
                elif (opcCarrera=='3'):
                    objetoCarrera.consultarCarrera(conex)
                elif (opcCarrera=='4'):
                    objetoCarrera.borrarInfoCarrera(conex)
                elif (opcCarrera=='5'):
                    borrar_tabla(conex)
                elif (opcCarrera=='6'):
                    salirCarrera=True
        elif (opcPrincipal=='2'):  #Condicional al elegir el 2
            salirAtletas=False
            while not salirAtletas:  #Ciclo mientras no salga del menu de administración de atletas
                opcAtletas=input('''
Menú Administración de Atletas
1  Crear un Atleta en la Base de Datos
2  Modificar información de un Atleta
3  Consultar información de un Atleta
4  Borrar información de un atleta
5  Borrar tabla
6  Salir
Opción seleccionada>>>:  ''')
                if (opcAtletas=='1'):  #Condicional que se ejecuta al elegir la opción 1
                    ObjetoAtleta.setNoIdAtleta()
                    ObjetoAtleta.setNoInscripcion()
                    ObjetoAtleta.setNombre()
                    ObjetoAtleta.setApellido()
                    ObjetoAtleta.setFechaNacimiento()
                    ObjetoAtleta.setPaisOrigen()
                    ObjetoAtleta.setCiudadOrigen()
                    atletacreado=ObjetoAtleta.setatleta()
                    ObjetoAtleta.insertar_atleta(conex, atletacreado)
                    pregunta = input("¿Desea que le enviemos un correo electronico confirmando su inscripcion?(si/no): ")
                    if (pregunta == "si"):
                        correo()
                elif (opcAtletas=='2'):  #Condicional que se ejecuta al elegir la opción 2
                    ObjetoAtleta.actualizar_atleta(conex)
                elif (opcAtletas=='3'):  #Condicional que se ejecuta al elegir la opción 3
                    ObjetoAtleta.consultar_atleta(conex)
                elif (opcAtletas=='4'):  #Condicional que se ejecuta al elegir la opción 4
                    ObjetoAtleta.borrar_info_atleta(conex)
                elif (opcAtletas=='5'):  #Condicional que se ejecuta al elegir la opción 5
                    borrar_tabla(conex)
                elif (opcAtletas=='6'):  #Condicional que se ejecuta al elegir la opción 6
                    salirAtletas=True
        elif (opcPrincipal=='3'):  #Condicional al elegir 3 en el menu principal
            salirResultado=False
            while not salirResultado:  #Ciclo mientras no se salga del menu de resultados de carrera
                opcResultado=input('''
Menú de administración Resultado Carrera
1  Ver resultado carrera
2  Crear un resultado carrera
3  Modificar información de un resultado carrera
4  Borrar tabla
5  Salir
Opción seleccionada>>>:  ''')
                if (opcResultado=='1'):  #Condicional para opción 1
                    objetoResultadoCarrera.mostrar_datos_ResultadoCarrera(conex)
                elif (opcResultado=='2'):
                    objetoResultadoCarrera.setNoEvento()
                    objetoResultadoCarrera.setNoInscripcion()
                    objetoResultadoCarrera.setPosicion()
                    objetoResultadoCarrera.setTiempoAtleta()
                    objetoResultadoCarrera.setIndicadorResultado()
                    objetoResultadoCarrera.setResultadoCarrera()
                    valores=objetoResultadoCarrera.setResultadoCarrera()
                    objetoResultadoCarrera.insertarResultado(conex,valores)
                elif (opcResultado=='3'):
                    objetoResultadoCarrera.ModificarResultado(conex)
                elif (opcResultado=='4'):
                    borrar_tabla(conex)
                elif (opcResultado=='5'):
                    salirResultado=True
        elif (opcPrincipal=='4'): #Condicional para opción 4 del menu princinpal
            salirConsulta=False
            while not salirConsulta:  #Ciclo que sucedera mientras no salgamos de Consulta clasificación final
                opcConsulta=input('''
Menú de Consulta de la Clasificación Final 
1  Consultar Clasificación general
2  Salir
Opción seleccionada>>>:  ''')  #Menú de Clasificación final
                if (opcConsulta=='1'):  #Condicional para opción 1
                    
                    
                        app = QApplication(sys.argv)    
                        MainWindow = QMainWindow()  #ventana del Menu
                        u = objetoClasificacion.Ui_Menu()   
                        u.setupUi(MainWindow)
                        MainWindow.show()   #aparece la ventana en la pantalla
                        app.exec_()     #procesa la ventana(botones, informacion, etc.)

                        Window2 = QMainWindow()
                        Ui2 = objetoClasificacion.Ui_ConsultaWindow()
                        Ui2.setupUi(Window2)
                        Ui2.mostrar_datos() # Llamar al método para mostrar los datos en la tabla
                        Window2.show()  #abrimos la ventana
                        app.exec_() #procesa la ventana(botones, informacion, etc.)
                elif (opcConsulta=='2'):
                    salirConsulta=True
        elif (opcPrincipal=='5'):  #Condicional al elegir 5 en el menu principal
            salirPrincipal=True
    print('Programa finalizado.  Gracias por utilizar nuestros servicios.') 
def menu(conex, objetoCarrera, objetoAtleta, objetoResultadoCarrera, objetoClasificacion):  #Definimos cual menu se usara 
    if autenticar_usuario():  #Si el usuario y la clave si son correctas ejecuta el menu de administrador 
        menu_administrador(conex, objetoCarrera, objetoAtleta, objetoResultadoCarrera, objetoClasificacion)
    else: 
        menu_usuario(conex, objetoCarrera, objetoAtleta, objetoResultadoCarrera, objetoClasificacion)  #Si el usuario y la clave son incorrectas ejecuta el menu del usuario
def cerrarConexionBD(con):  #En esta funcion cerraremos la conexion con la base de datos
    con.close()
def main():  #Aca definimos que se va a ejecutar
    conex=conexion_db()
    crear_tabla_atleta(conex)
    crear_tabla_ClasificacionFinal(conex)
    CrearTablaCarrera(conex)
    CrearTablaResultadoCarrera(conex)
    objetoCarrera = Carrera()
    objetoAtleta = Atleta()
    objetoResultadoCarrera=ResultadoCarrera()
    objetoClasificacion=ClasificacionFinal()
    menu(conex, objetoCarrera, objetoAtleta, objetoResultadoCarrera, objetoClasificacion)
    cerrarConexionBD(conex)
main()  #Ejecutamos el main