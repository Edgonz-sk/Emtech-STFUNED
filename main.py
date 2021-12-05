import pandas as pd
import itertools
from datos import products, sales, searches
from pdf import pdf
global cuentas

# Se hace un cruce entre la tabla de ventas y productos
sales = pd.merge(left=sales, right=products, on='id_producto', how='left')
# Se hace un cruce entre la tabla de busquedas y productos
searches = pd.merge(left=searches, right=products, on='id_producto', how='left')

# print(searches.head().to_string())

# Lista de cuentas existentes en el reporteador
cuentas = [{'usuario': 'Paulo', 'contrasenia': 'Leonesconflow'},
           {'usuario': 'Londra', 'contrasenia': 'Leonesconflow'},
           {'usuario': '1', 'contrasenia': '1'}]

# Funcion de ingreso de cuenta
def ingreso():
    intentos = 0
    # Se dan 3 oportunidades para ingresar usuario y contrasenia correctamente
    while intentos < 3:
        usuario = input('Ingrese su nombre de usuario: ')
        if any(diccionario['usuario'] == usuario for diccionario in cuentas):
            contrasenia = input('Ingrese contrasenia: ')
            # Si se encuentra la contrasenia en la lista de cuentas, se acepta y se detiene el ciclo
            if contrasenia in [usuarios['contrasenia'] for usuarios in cuentas if usuarios['usuario'] == usuario]:
                key = True
                break
            else:
                print('Conatrasenia incorrecta. Intente nuevamente\n')
        else:
            print('Usuario no existente en la base de datos. Intente nuevamente\n')
        intentos += 1
        key = False
    return key
# Funcion de registro de cuenta
def registro():
    cuenta_nueva_valida = False
    while not cuenta_nueva_valida:
        print('Creando cuenta nueva')
        print('--------------------')
        # El usuario ingresa los datos de la nueva cuenta
        usuario_nuevo = input('Nuevo nombre de usuario: ')
        contrasenia_nueva = input('Contrasenia: ')
        # Si no existe otro usuario con el mismo nombre, la cuenta es valida
        if not any(diccionario['usuario'] == usuario_nuevo for diccionario in cuentas) or usuario_nuevo != 'nuevo':
            cuenta_nueva_valida = True
            print('La cuenta fue agregada con exito')
            cuentas.append({'usuario': usuario_nuevo, 'contrasenia': contrasenia_nueva})
        else:
            print('Este nombre de usuario ya existe. Favor de intentar con otro')
            continue
    return cuenta_nueva_valida

print("----------------------------")
print("\x1B[3mLifestore es tu mejor opción\x1B[0m")
print("----------------------------\n")
print("¡Bienvenido!")
print("Este es un reportador para el área de ventas de Lifestore")
print("-------------------------------------------------------------")
print('1) Inicio de sesion')
print('2) Registro de cuenta')
ingreso_ciclo = int(input())


# Se crea un ciclo para que el usuario inicie sesion
while True:
    if ingreso_ciclo == 1:
        llave = ingreso()
        break
    elif ingreso_ciclo == 2:
        registro()
        llave = ingreso()
        break
    else:
        ingreso_ciclo = int(input('\nIngrese una opcion valida:'))

# Si inicio sesion correctamente entonces 'llave' permite generar el reporte
if llave:
    print('Bievenido!')
    print('Generando reporte...\n')

    # Se imprimen el top 5 ventas en los ultimos 3 meses
    top = list()
    print("Los 5 productos con mayores ventas en los ultimos 3 meses")
    for mes_anio in sales['Mes_anio'].sort_values().unique()[-3:]:
      print("")
      print(pd.to_datetime(mes_anio).strftime('%B %Y'))
      top5_sales = sales[sales['Mes_anio'] == mes_anio].groupby('Nombre').agg(Ventas=('Precio', 'size'), Ingreso=('Precio', 'sum')).sort_values(by='Ventas', ascending=False).head()
      print(top5_sales)
      top.append(top5_sales)
    print("-------------------------------------------------------\n")

    # Se imprimen el top 10 busquedas
    print("Los 10 productos con mayores busquedas")
    top10_searches = searches.groupby('Nombre').agg(Busquedas=('Precio', 'size')).sort_values(by='Busquedas', ascending=False).head(10)
    print(top10_searches)
    top.append(top10_searches.index)
    print("-------------------------------------------------------\n")

    # Se imprimen el bottom 10 ventas en los ultimos 3 meses
    bottom = list()
    print("Los 5 productos con menores ventas en los ultimos 3 meses")
    for mes_anio in sales['Mes_anio'].sort_values().unique()[-3:]:
      print("")
      print(pd.to_datetime(mes_anio).strftime('%B %Y'))
      bottom5_sales = sales[sales['Mes_anio'] == mes_anio].groupby('Nombre').agg(Ventas=('Precio', 'size'), Ingreso=('Precio', 'sum')).sort_values(by='Ventas').head()
      print(bottom5_sales)
      bottom.append(bottom5_sales.index)
    print("-------------------------------------------------------\n")
    
    # Se imprimen el bottom 10 busquedas
    print("Los 10 productos con menores busquedas")
    bottom10_searches = searches.groupby('Nombre').agg(Busquedas=('Precio', 'size')).sort_values(by='Busquedas').head(10)
    print(bottom10_searches)
    bottom.append(bottom10_searches)
    print("-------------------------------------------------------\n")

    # De los productos mas vendidos y buscados se obtiene el puntaje promedio
    print("Las mejores 5 resenias de los productos mas vendidos y buscados")
    top = list(itertools.chain(*top))
    top5_scores = sales[sales['Nombre'].isin(top)].groupby('Nombre').agg(Puntaje_prom=('Puntaje', 'mean')).sort_values(by='Puntaje_prom',ascending=False).head().round(1)
    print(top5_scores)
    print("-------------------------------------------------------\n")

    # De los productos menos vendidos y buscados se obtiene el puntaje promedio
    print("Las peores 5 resenias de los productos menos vendidos y buscados")
    bottom = list(itertools.chain(*bottom))
    bottom5_scores = sales[sales['Nombre'].isin(top)].groupby('Nombre').agg(Puntaje_prom=('Puntaje', 'mean')).sort_values(by='Puntaje_prom').head().round(1)
    print(bottom5_scores)
    print("-------------------------------------------------------\n")

    # Total de ventos e ingresos promedio por mes
    print("Total ventas e ingresos promedio por mes")
    meses = sales.groupby('Mes_anio').agg(Ventas=('Precio', 'size'), Ingresos=('Precio', 'sum')).mean().round()
    print(meses.to_string())
    print("-------------------------------------------------------\n")

    # Total de ventas e ingresos anual 
    print("Total ventas e ingresos anual")
    anuales = sales.groupby("Anio").agg(Ventas=('Precio', 'size'), Ingresos=('Precio', 'sum'))
    print(anuales)
    print("-------------------------------------------------------\n")

    # Los 5 meses con mas ventas del anio
    print("Meses con más ventas del anio")            
    mes = sales.groupby('Mes').agg(Ventas=('Precio', 'size')).sort_values(by='Ventas', ascending=False).head()
    print(mes)

    # ADICIONAL: El usuario podra guardar sus resultados en un PDF
    print('¿Desea guardar el reporte como archivo PDF?')
    guardar = input("'si' para iniciar la descarga o cualquier otra tecla para cancelar\n")
    if guardar == 'si':
      pdf(sales, top10_searches, bottom10_searches, top5_scores, bottom5_scores, meses, anuales, mes)
    else:
      pass
    print('\nGracias por confiar en EmTech')
    print('¡Hasta luego!')
else:
    print('Acceso denegado')