import numpy as np
import random
from pyrecord import Record

# Una entidad bancaria tiene organizada su información en los siguientes vectores de registros:
#        [CUENTAS]   datos de los clientes
#        [CAJEROS]   datos de los cajeros automáticos

# Y el archivo de texto
#        [OPERACIONES.TXT] datos de los movimientos realizados por los clientes en los cajeros.

# Las estructuras de cada uno son las siguientes:
#   “CUENTAS”
#        Numero_cuenta: Integer;
#        Apellido: String [50];
#        Nombre: String [50];
#        DNI: String [8]
#        Tipo_Cuenta: (1 al 15): Integer
#        Saldo: Real;
#        Activa: Booleano (True=Activa, False=Inactiva dada de baja)

#  “CAJEROS”
#        Numero_cajero: Integer;     (1 al 120)
#        Ubicacion: String [50];
#        Cant_mov: Integer;          (Cantidad histórica de movimientos)

# ARCHIVO “OPERACIONES.TXT” (Secuencial de Texto)
# Número de cuenta:    Integer
# Año:    Integer
# Mes:    Integer
# Día:    Integer
# Número de cajero (0 – 119) :    Integer
# Tipo de movimiento (1 = depósito, 2 = extracción)
# Monto en pesos:      (real)

# El archivo se encuentra ordenado por número de cuenta y dentro de número de cuenta por fecha.

#CONSIGNAS --------------------------------------------------------------------------------------

# Se solicita realizar un programa que contenga las funciones y/o procedimientos necesarios para
# cumplir con las siguientes consignas:

# 1) Realizar consulta de saldo de cualquier cuenta, ingresando por teclado el número de cuenta.

# 2) Procesar el archivo de movimientos, utilizando la técnica de corte de control, para:
#        A) Informar el total anual (en $) de los movimientos de cada una de las cuentas.
#        B) Informar que cajero registró mayor cantidad de movimientos durante el año.
#        C) Actualizar el saldo de las cuentas en CUENTAS.
#        D) Actualizar la cantidad de movimientos de cada cajero en CAJEROS

# 3) Realizar ABM sobre CUENTAS
#        A Altas de nuevas cuentas
#        B Borrado de cuentas, solo se pone Activa en False
#        M Modificaciones como Apellido, Nombre, DNI y Tipo de cuenta

#        - Considerar que cada cliente puede tener solamente 1 cuenta en el banco. Al realizar un alta 
#          debe verificarse que no exista una cuenta activa para el mismo DNI.
#        - La numeración de las nuevas cuentas debe ser consecutiva

# -----------------------------------------------------------------------------------------------
# RESTRICCIÓN: El  archivo  OPERACIONES.TXT puede  leerse  por  completo solamente 
# Una Vez en todo el programa durante el corte de Control.

r_cuentas = Record.create_type("r_cuentas","Numero_cuenta","Apellido","Nombre","DNI","Tipo_Cuenta","Saldo","Activa",Numero_cuenta=0,Apellido="",Nombre="",DNI="",Tipo_Cuenta=0,Saldo=0.0,Activa=True)
v_cuentas = np.array([r_cuentas] * 650)
r_cajeros = Record.create_type("r_cajeros","Numero_cajero","Ubicacion","Cant_mov",Numero_cajero=0,Ubicacion="",Cant_mov=0)
v_cajeros = np.array([r_cajeros] * 120)
freq_cajeros = np.array([0] * 120)

#Cargar vector CUENTAS
def cargar_cuentas(v):

    a1 = open("cuentas.txt","r")
    linea = a1.readline().strip()

    for i in range(0,600):

        v[i] = r_cuentas()
        s=linea.split(',')

        v[i].Numero_cuenta = int(s[0])
        v[i].Apellido = str(s[1])
        v[i].Nombre = str(s[2])
        v[i].DNI = str(s[3])
        v[i].Tipo_Cuenta = int(s[4])
        v[i].Saldo = float(s[5])
        v[i].Activa = bool(s[6])
        linea = a1.readline().strip()
    
    for x in range(600,len(v)):

        v[x] = r_cuentas()
        v[x].Numero_cuenta = 0
        v[x].Apellido = ""
        v[x].Nombre = ""
        v[x].DNI = ""
        v[x].Tipo_Cuenta = 0
        v[x].Saldo = 0.0
        v[x].Activa = False

    dar_de_alta1600(v)
    a1.close()
    return v

#Mostrar vector CUENTAS
def print_v_cuentas(v):
    print()
    for i in range(len(v)):
        if v[i].Activa:
            print(f"Nro. cuenta: {v[i].Numero_cuenta}, DNI: {v[i].DNI}")
            print(f"Apellido y nombre: {v[i].Apellido}, {v[i].Nombre}")
            print(f"Tipo de cuenta: {v[i].Tipo_Cuenta}, SALDO: {v[i].Saldo}")
            print("-"*50)
    print()      

#Cargar vector CAJEROS
def cargar_cajeros(v):

    a1 = open("cajeros.txt","r")
    linea = a1.readline().strip()

    for i in range(len(v)):

        v[i] = r_cajeros()
        s = linea.split(",")

        v[i].Numero_cajero = int(s[0])
        v[i].Ubicacion = str(s[1])
        v[i].Cant_mov = int(s[2])
        linea = a1.readline().strip()

    a1.close()
    return v

#Mostrar vector CAJEROS
def print_v_cajeros(v):
    print()
    print(f"Nro. cajero         Ubicacion         Cant. de mov.")
    print("-"*50)
    for i in range(len(v)):
        print(f"   {v[i].Numero_cajero:>3}       {v[i].Ubicacion:>20}         {v[i].Cant_mov:>5}")
    print()

#Mostrar saldo de la cuenta ingresada por teclado
def buscar_cuenta_teclado(v_cuentas):
    #valor = ingresar_valor(max)
    max = buscar_siguiente(v_cuentas) - 1
    teclado = input(f"Ingrese un número de cuenta (entre 1000 y {max+1000}): ")

    while not teclado.isnumeric():
        print("[ERROR]: Cadena no numérica, intente otra vez")
        teclado = input(f"Ingrese un número de cuenta (entre 1000 y {max+1000}): ")

    valor = int(teclado)
    print()
    i = 0
    num_cuenta = v_cuentas[i].Numero_cuenta
    while num_cuenta != valor and i < (len(v_cuentas)-1):
        i += 1
        num_cuenta = v_cuentas[i].Numero_cuenta

    if valor == v_cuentas[i].Numero_cuenta and v_cuentas[i].Activa:
        clear_screen()
        print(f"Saldo de la cuenta número {valor}: {v_cuentas[i].Saldo}")
    else:
        clear_screen()
        print("[CUENTA NO ENCONTRADA]")
    print()

#Consigna 2
def consigna(v_cuentas,v_cajeros,freq_cajeros):
    a1 = open("OPERACIONES.TXT","r")

    linea = a1.readline().strip()
    s = linea.split(",")
    num_cuenta = int(s[0])
    print()
    print(f"[Nro. Cuenta]       [Total mov.]")
    print()
    i = 0
    while linea != "":

        suma_mov = 0
        num_cuenta_ant = num_cuenta

        while linea != "" and num_cuenta_ant == num_cuenta:

            numero_cajero = int(s[4]) - 1

            v_cajeros[numero_cajero].Cant_mov += 1

            freq_cajeros[numero_cajero] += 1 

            monto = float(s[6])
            tipo_mov = int(s[5])

            if tipo_mov == 2:
                monto *= -1
            suma_mov += monto

            linea = a1.readline().strip()

            if linea != "":
                s = linea.split(",")
                num_cuenta = int(s[0])
        
        print(f"    {num_cuenta_ant}:       $ {suma_mov}")
        v_cuentas[i].Saldo += suma_mov
        i += 1
    print()
    buscar_mayor_cajeros(freq_cajeros)
    print()
    a1.close()
    input("Presione [ENTER] para continuar: ")

#Buscar cajero con mayor cantidad de movimientos
def buscar_mayor_cajeros(f):
    mayor = 0
    cajero = 0
    iguales = 0
    for i in range(len(f)):
        if f[i] > mayor:
            iguales = 0
            mayor = f[i]
            cajero = i + 1
        elif f[i] == mayor:
            iguales += 1
    print()
    print(f"El cajero con mayor cantidad de movimientos en el año fue el [{cajero}] con [{mayor}] movimientos, compartiendo esta cantidad con [{iguales}] cajeros")
    return cajero

#Dar de alta una cuenta
def dar_alta(v_cuentas):

    dni = input("Ingrese su DNI (o presione [ENTER] para [SALIR]): ")
    if dni.isnumeric():
        repetido = 0
        for i in range(len(v_cuentas)):
            if dni == v_cuentas[i].DNI:
                repetido = 1
                cuenta_repetida = i

        if repetido == 0:
            clear_screen()
            apellido = str(input("Ingrese su apellido: "))
            while not apellido.isalpha():
                clear_screen()
                print("[ERROR]: La cadena ingresada contiene caracteres no alfabéticos")
                apellido = str(input("Ingrese su apellido: "))
            clear_screen()
            nombre = str(input("Ingrese su nombre: "))
            while not nombre.isalpha():
                clear_screen()
                print("[ERROR]: La cadena ingresada contiene caracteres no alfabéticos")
                nombre = str(input("Ingrese su nombre: "))
            clear_screen()
            tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))
            while not tipo_cuenta.isnumeric() or (int(tipo_cuenta) > 15 or int(tipo_cuenta) < 1):
                clear_screen()
                if not tipo_cuenta.isnumeric():
                    print("[ERROR]: La cadena ingresada contiene caracteres no numéricos")
                    tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))
                else:
                    print("[ERROR]: Tipo de cuenta no válida")
                    tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))
        
            #saldo = "A"
            clear_screen()
            saldo = float(input("Ingrese su saldo (no mienta) (: "))

            MAX_V = buscar_siguiente(v_cuentas)

            v_cuentas[MAX_V].Numero_cuenta = 1000 + MAX_V
            v_cuentas[MAX_V].Apellido =str(apellido)
            v_cuentas[MAX_V].Nombre = str(nombre)
            v_cuentas[MAX_V].DNI = str(dni)
            v_cuentas[MAX_V].Tipo_Cuenta = int(tipo_cuenta)
            v_cuentas[MAX_V].Saldo = saldo
            v_cuentas[MAX_V].Activa = True

            clear_screen()
            print("Cuenta creada satisfactiriamente")
            print()
            input("Presione [ENTER] para continuar: ")
        else:
            clear_screen()
            print("[ERROR]: DNI ya registrado")
            print(f"Cuenta nro: {v_cuentas[cuenta_repetida].Numero_cuenta}, DNI: {v_cuentas[cuenta_repetida].DNI}, Saldo: {v_cuentas[cuenta_repetida].Saldo}")
            print()
            dar_alta(v_cuentas)
    else:
        if dni != "":
            print()
            print("[ERROR]: Se ingreso una cadena no numerica")
            dar_alta(v_cuentas)

    return v_cuentas, MAX_V
        
#Borrado de cuentas
def borrar_cuenta(vc):
    clear_screen()
    nro = input("Ingrese el numero de la cuenta que desea borrar (o presione [ENTER] para [SALIR]): ")
    if nro.isnumeric():
        encontrada = 0
        for i in range(len(vc)):
            if int(nro) == vc[i].Numero_cuenta:
                encontrada = 1
                index_cuenta = i
        if encontrada == 1:
            clear_screen()
            print(f"Se eliminó la cuenta nro. {nro} satisfactoriamente")
            vc[index_cuenta].Activa = False
            print()
            input("Presione [ENTER] para continuar: ")
        else:
            clear_screen()
            print("[ERROR]: Cuenta no encontrada")
            borrar_cuenta(vc)
    else:
        if nro != "":
            clear_screen()
            print("[ERROR]: Se ingreso una cadena no numerica")
            borrar_cuenta(vc)
    return vc

#Modificar una cuenta
def modificar_cuenta(v_cuentas):

    nro_cuenta = input("Ingrese su número de cuenta (o presione [ENTER] para [SALIR]): ")
    if nro_cuenta.isnumeric():
        encontrada = 0
        for i in range(len(v_cuentas)):
            if int(nro_cuenta) == v_cuentas[i].Numero_cuenta:
                encontrada = 1
                index_cuenta = i

        if encontrada == 1:
            print("[1]: Modificar apellido")
            print("[2]: Modificar nombre")
            print("[3]: Modificar DNI")
            print("[4]: Modificar tipo de cuenta")
            print()
            mod = input("Ingrese la modificación a realizar: ")

            while not mod.isalnum() or (int(mod)<1 or int(mod)>4):
                clear_screen()
                print("[ERROR]: Acción inválida")
                print()
                print("[1]: Modificar apellido")
                print("[2]: Modificar nombre")
                print("[3]: Modificar DNI")
                print("[4]: Modificar tipo de cuenta")
                print()
                mod = input("Ingrese la modificación a realizar: ")

            clear_screen()

            if int(mod) == 1:
                apellido = str(input("Ingrese su apellido: "))
                while not apellido.isalpha():
                    clear_screen()
                    print("[ERROR]: La cadena ingresada contiene caracteres no alfabéticos")
                    apellido = str(input("Ingrese su apellido: "))
                v_cuentas[index_cuenta].Apellido =str(apellido.upper())

            elif int(mod) == 2:
                nombre = str(input("Ingrese su nombre: "))
                while not nombre.isalpha():
                    clear_screen()
                    print("[ERROR]: La cadena ingresada contiene caracteres no alfabéticos")
                    nombre = str(input("Ingrese su nombre: "))
                v_cuentas[index_cuenta].Nombre = str(nombre.upper())

            elif int(mod) == 3:
                DNI = str(input("Ingrese su DNI: "))
                while not DNI.isnumeric():
                    clear_screen()
                    print("[ERROR]: La cadena ingresada contiene caracteres no numéricos")
                    DNI = str(input("Ingrese su DNI: "))
                v_cuentas[index_cuenta].DNI = str(DNI)

            else:
                tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))

                while not tipo_cuenta.isnumeric() or (int(tipo_cuenta) > 15 or int(tipo_cuenta) < 1):
                    clear_screen()
                    if not tipo_cuenta.isnumeric():
                        print("[ERROR]: La cadena ingresada contiene caracteres no numéricos")
                        tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))
                    else:
                        print("[ERROR]: Tipo de cuenta no válida")
                        tipo_cuenta = str(input("Ingrese su tipo de cuenta(1-15): "))

                v_cuentas[index_cuenta].Tipo_Cuenta = int(tipo_cuenta)
                    
            clear_screen()
            print("Cuenta modificada satisfactiriamente")
            print()
            input("Presione [ENTER] para continuar: ")
        else:
            clear_screen()
            print("[ERROR]: Cuenta no encontrada")
            print()
            modificar_cuenta(v_cuentas)
    else:
        if nro_cuenta != "":
            clear_screen()
            print("[ERROR]: Se ingreso una cadena no numérica")
            print()
            modificar_cuenta(v_cuentas)

    return v_cuentas

#Dar de alta cuenta 1600
def dar_de_alta1600(v):
    v[600].Numero_cuenta = 1600
    v[600].Apellido = "MONTI"
    v[600].Nombre = "KEVIN"
    v[600].DNI = "44003780"
    v[600].Tipo_Cuenta = 2
    v[600].Saldo = 1.577819508584496E+004
    v[600].Activa = True

def clear_screen():
    for i in range(50):
        print()

#Buscar el seguiente indice al maximo indice
def buscar_siguiente(v):
    i = 0
    while v[i].Activa:
        i += 1
        ult_valor = i
    return ult_valor


# 3) Realizar ABM sobre CUENTAS
#        A Altas de nuevas cuentas [CASI]
#        B Borrado de cuentas, solo se pone Activa en False
#        M Modificaciones como Apellido, Nombre, DNI y Tipo de cuenta

#        - Considerar que cada cliente puede tener solamente 1 cuenta en el banco. Al realizar un alta 
#          debe verificarse que no exista una cuenta activa para el mismo DNI.
#        - La numeración de las nuevas cuentas debe ser consecutiva


#MAIN BOOTY
cargar_cuentas(v_cuentas)
cargar_cajeros(v_cajeros)
consigna(v_cuentas,v_cajeros,freq_cajeros)
#buscar_cuenta_teclado(v_cuentas)

#print_v_cajeros(v_cajeros)
#print_v_cuentas(v_cuentas)

#dar_alta(v_cuentas)

#modificar_cuenta(v_cuentas)
#borrar_cuenta(v_cuentas)


