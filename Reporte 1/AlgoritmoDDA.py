import matplotlib.pyplot as plt

def dibujar_linea_DDA(x1, y1, x2, y2):
    """
    Args utilizados:
        x1 (float): Coordenada x del punto de inicio.
        y1 (float): Coordenada y del punto de inicio.
        x2 (float): Coordenada x del punto final.
        y2 (float): Coordenada y del punto final.
    """
    # Nombramos como dx y dy las diferencias en las coordenadas
    dx = x2 - x1
    dy = y2 - y1

    #Determinamos el número de pasos
    # El número de pasos es el máximo entre el valor absoluto de dx y dy.
    # Esto asegura que la línea se trace correctamente, independientemente de la pendiente.
    pasos = int(max(abs(dx), abs(dy)))

    #Calculamos los incrementos en cada eje
    # Si los pasos son igualn a 0, no hay línea, por lo que no hay incremento.
    x_incremento = dx / pasos if pasos != 0 else 0
    y_incremento = dy / pasos if pasos != 0 else 0

    # Listas para almacenar los píxeles de la línea
    x_puntos = []
    y_puntos = []

    #Inicializamos coordenadas iniciales
    x = x1
    y = y1

    #Iterar para trazar la línea
    for _ in range(pasos + 1):
        # Almacenar el pixel actual (redondeado)
        x_puntos.append(round(x))
        y_puntos.append(round(y))
        
        # Incrementar las coordenadas para el siguiente píxel
        x += x_incremento
        y += y_incremento

    #Visualizar la línea con Matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(x_puntos, y_puntos, 's-', markersize=5, label='Línea DDA')
    plt.scatter([x1, x2], [y1, y2], color='red', s=100, zorder=5, label='Puntos P1 y P2')
    plt.title('Ejemplito del Algoritmo DDA :D')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.grid(True)
    plt.axis('equal') # Asegura que la escala de los ejes sea la misma
    plt.legend()
    plt.show()

# Aqui cambiar valores 
x_inicio, y_inicio = 200, 225.4
x_fin, y_fin = 100, 800

dibujar_linea_DDA(x_inicio, y_inicio, x_fin, y_fin)