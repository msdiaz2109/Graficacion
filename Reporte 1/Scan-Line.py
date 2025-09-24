import pygame
import numpy as np

def scan_line_fill(surface, polygon_points, fill_color):
    """
    Idea principal: Rellenar un polígono utilizando el algoritmo Scan-Line.
    Args utilizados:
        surface: La superficie de Pygame donde se dibujará.
        polygon_points: Una lista de tuplas (x, y) que definen los vértices del polígono.
        fill_color: Una tupla (R, G, B) con el color de relleno.
    """
    if not polygon_points or len(polygon_points) < 3:
        return

    # Convertir los puntos a un array de NumPy para un manejo más sencillo
    points = np.array(polygon_points, dtype=np.int32)
    
    # Encontrar los límites del polígono
    min_y = np.min(points[:, 1])
    max_y = np.max(points[:, 1])
    
    # Bucle principal para cada línea de escaneo
    for y in range(min_y, max_y + 1):
        intersections = []
        num_points = len(points)
        
        # Encontrar las intersecciones entre la línea de escaneo y los bordes del polígono
        for i in range(num_points):
            p1 = points[i]
            p2 = points[(i + 1) % num_points]
            
            # Asegurarse de que el borde cruza la línea de escaneo
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                # Evitar división por cero si el borde es horizontal
                if p1[1] != p2[1]:
                    # Calcular la intersección en x
                    x_intersect = int(p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]))
                    intersections.append(x_intersect)
        
        # Ordenar las intersecciones de menor a mayor
        intersections.sort()
        
        # Rellenar los píxeles entre las intersecciones
        # Dibujar líneas horizontales entre pares de puntos de intersección
        for i in range(0, len(intersections), 2):
            x1 = intersections[i]
            x2 = intersections[i + 1] if i + 1 < len(intersections) else x1
            pygame.draw.line(surface, fill_color, (x1, y), (x2, y))

# iniciamos el Pygame
pygame.init()
width, height = 800, 600    
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scan-Line jeje")

# Colorsitos
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Puntos del polígono de ejemplo (un pentágono)
polygon_points = [(400, 100), (600, 300), (500, 500), (300, 500), (200, 300)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Borrar pantalla
    screen.fill(black)
    
    # Rellenar el polígono con el algoritmo Scan-Line
    scan_line_fill(screen, polygon_points, red)
    
    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()