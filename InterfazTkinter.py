#Librería para interacción por consola (interfaz)
#################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#Presentar mensaje genérico en pantalla
def mensaje(info=''):
    print()
    print(info)
    print()

#Formulario menú aplicación CRUD
ventana = tk.Tk()
tree = ttk.Treeview(
    ventana, height=10, selectmode='browse', columns=[f"#{n}" for n in range(1, 5)]
)
persistencia = None

def formularioMenuAppCRUD(tareas, crud):
    persistencia = crud
    ventana.title("CRUD")
    ventana.config(width=800, height=600)
    tree.config(show='headings')
    tree.grid(row=1, column=1, columnspan=4, padx=20, pady=20)
    tree.heading('#1', text='ID')
    tree.heading('#2', text='Descripción')
    tree.heading('#3', text='Estado')
    tree.heading('#4', text='Tiempo')
    mostrarTareas(tareas)
    l0 = tk.Label(ventana,  text='Agregar Tarea',
                  font=('Helvetica', 16), width=30, anchor="c")
    l0.grid(row=2, column=1, columnspan=4)
    
    l1 = tk.Label(ventana,  text='ID: ', width=10, anchor="c")
    l1.grid(row=3, column=1)
    t1 = tk.Text(ventana,  height=1, width=10, bg='white')
    t1.grid(row=3, column=2)
    
    l2 = tk.Label(ventana,  text='Descripción: ', width=10)
    l2.grid(row=3, column=3)
    t2 = tk.Text(ventana,  height=1, width=10, bg='white')
    t2.grid(row=3, column=4)
    
    l3 = tk.Label(ventana,  text='Estado: ', width=10)
    l3.grid(row=4, column=1)
    radio_v = tk.StringVar()
    radio_v.set('pendiente')
    r1 = tk.Radiobutton(ventana, text='Pendiente', variable=radio_v, value='pendiente')
    r1.grid(row=4, column=2)
    r2 = tk.Radiobutton(ventana, text='Realizado', variable=radio_v, value='realizado')
    r2.grid(row=5, column=2)
    
    l4 = tk.Label(ventana,  text='Tiempo: ', width=10)
    l4.grid(row=4, column=3)
    options = tk.StringVar(ventana)
    options.set("")  # default value
    opt1 = tk.OptionMenu(ventana, options, 10, 20, 30, 40, 50, 60)
    opt1.grid(row=4, column=4)
    
    b1 = tk.Button(ventana,  text='Agregar Tarea', width=10,
                   command=lambda: formularioAdicionarTarea(t1, t2, radio_v, options, tareas, persistencia))
    b1.grid(row=6, column=2)
    
    ventana.mainloop()

#Función de validación en la colección recibida del controlador


def estaElemento(identificador, tareas):

    #Extraer de la base de datos (contenedor) los identificadores
    conjuntoIdentificadores = set(tareas.keys())
    #print(conjuntoIdentificadores, identificador)
    #Revisar si se encuentra el elemento solicitado
    if identificador in conjuntoIdentificadores:
        return True
    else:
        return False

#Formulario para adicionar tareas (Create)


def formularioAdicionarTarea(campo_id, campo_descripcion, campo_estado, campo_tiempo, tareas, persistencia):
    id = campo_id.get("1.0", "end")[:-1]
    descripcion = campo_descripcion.get("1.0", "end")[:-1]
    estado = campo_estado.get()
    tiempo = campo_tiempo.get()
    if not estaElemento(id, tareas):
        tareaNueva = {
            'descripcion': descripcion,
            'estado': estado,
            'tiempo': tiempo
        }
        persistencia.Create(tareas, id, tareaNueva)
        if persistencia.Write(tareas):
            #Solicitar a la interfaz reporte de salida exitosa
            messagebox.showinfo("Exito", "Datos guardados: Cierre exitoso.")
        tree.insert("", 'end', iid=id,
                    values=(id, descripcion, estado, tiempo))
    else:
        messagebox.showerror("Error", "El id de la tarea ya existe")

#Formulario para actualización de tareas


def formularioActualizarTarea(tareas):

    #Solicitar al usuario el identificador
    identificador = input("Ingrese identificador de la Tarea para modificar: ")

    #Revisar si se encuentra el elemento solicitado
    if estaElemento(identificador, tareas):

        #Recolectar los nuevos datos
        nuevaDescripcion = str(input('Nueva descripción: '))
        nuevoEstado = str(input('Nuevo estado: '))

        #Capturar el tiempo validando el tipo de dato ingresado
        nuevoTiempo = ''  # Alternativa a nulo, para conservar el tiempo anterior
        try:
            nuevoTiempo = int(input('Nuevo tiempo de realización: '))
        except:
            print("Entrada inválida: Se debe ingresar un tiempo numérico.")

        #Encapsular la tarea actualizada
        tareaActualizada = {
            'descripcion': nuevaDescripcion,
            'estado': nuevoEstado,
            'tiempo': nuevoTiempo
        }

        #Retornar el identificador de la tarea con los campos actualizados
        return identificador, tareaActualizada

    else:

        print("No ha sido encontrada la Tarea para actualización!")
        return False

#Formulario para eliminación de tareas


def formularioEliminarTarea(tareas):

    #Solicitar al usuario el identificador
    identificador = input("Ingrese identificador de la Tarea para eliminar: ")
    return identificador
    #Revisar si se encuentra el elemento solicitado para autorizar eliminado en el controlador
    #if estaElemento(identificador, tareas):
        #Retornar la bandera y el identificador para que el controlador elimine
        #return identificador
    #else:
        #print("No ha sido encontrada la Tarea para eliminación!")
        #return False

#Presentación de las tareas que llegan del controlador


def mostrarTareas(tareas):
    for identificador, tarea in tareas.items():
        tree.insert("", 'end', iid=identificador,
                    values=(identificador, tarea['descripcion'],
                            tarea['estado'], tarea['tiempo']))
