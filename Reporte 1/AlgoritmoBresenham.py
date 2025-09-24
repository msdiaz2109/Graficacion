import matplotlib.pyplot as plt

def dibujar_linea_bresenham(x1, y1, x2, y2):
    """
        x1 (int): Coordenada x del punto de inicio.
        y1 (int): Coordenada y del punto de inicio.
        x2 (int): Coordenada x del punto final.
        y2 (int): Coordenada y del punto final.
    """
    # Listas para almacenar los píxeles
    x_puntos = []
    y_puntos = []

    # esto asegura que la línea siempre se trace de izquierda a derecha.
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    # Iniciamos las coordenadas
    x = x1
    y = y1
    
    # Parámetro de decisión inicial
    # Se multiplica por 2 para usar solo enteros
    p = 2 * dy - dx

    # Trazamos la línea si la pendiente es menor o igual a 1 (m <= 1)
    if abs(dy) <= dx:
        for _ in range(dx + 1):
            x_puntos.append(x)
            y_puntos.append(y)
            
            x += 1
            if p < 0:
                p += 2 * dy
            else:
                y += 1
                p += 2 * (dy - dx)
    
    # Trazamos la línea si la pendiente es mayor a 1 (m > 1)
    else:
        # Se intercambian dx y dy para el cálculo del parámetro
        dx, dy = abs(dy), abs(dx)
        p = 2 * dy - dx
        
        # Se intercambian x e y para trazar
        x_temp = x
        y_temp = y
        
        for _ in range(dx + 1):
            x_puntos.append(x_temp)
            y_puntos.append(y_temp)
            
            y_temp += 1
            if p < 0:
                p += 2 * dy
            else:
                x_temp += 1
                p += 2 * (dy - dx)
    
    # Visualizar la línea con Matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(x_puntos, y_puntos, 'o-', markersize=5, label='Línea Bresenham')
    plt.scatter([x1, x2], [y1, y2], color='red', s=100, zorder=5, label='Puntos P1 y P2')
    plt.title('Increible Línea con el Algoritmo de Bresenham XD')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()

# Aqui se cambian las variables
x_inicio, y_inicio = 500, 200
x_fin, y_fin = 900, 800

dibujar_linea_bresenham(x_inicio, y_inicio, x_fin, y_fin)
