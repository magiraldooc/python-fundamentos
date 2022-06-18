#Aplicación CRUD (Controlador) - Lista de Tareas Pendientes
###########################################################

#Librerías (capas)
import CRUD  # Capa lógica o backend básico
import InterfazTkinter as ic  # Interfaz para interacción con el usuario UI
import sys  # API para comunicar la App con funciones del sistema operativo

#Carga de la base de datos de la aplicación (archivo json)
tareas = CRUD.Read()
if not(tareas):  # Si no se obtiene el listado de tareas del archivo json (Base de Datos)
    sys.exit(1)  # Terminación de la App reportando error

#Iniciar Mainloop de la App
#--------------------------
ic.formularioMenuAppCRUD(tareas, CRUD)
#ic.mostrarTareas(tareas)
