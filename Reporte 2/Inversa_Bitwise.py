from PIL import Image
import numpy as np
import pygame

# Cargar la imagen
imagen = Image.open('pruebaimagen.jpeg').convert('RGB')
arr = np.array(imagen)

# Inversión de colores usando operación bitwise NOT
arr_invertida = np.bitwise_not(arr)

# Guardar la imagen invertida
imagen_invertida = Image.fromarray(arr_invertida)
# Inicializar pygame
pygame.init()

# Convertir imágenes de numpy array a superficie de pygame
def numpy_to_surface(arr):
    return pygame.surfarray.make_surface(np.transpose(arr, (1, 0, 2)))

# Crear superficies para ambas imágenes
surface_original = numpy_to_surface(arr)
surface_invertida = numpy_to_surface(arr_invertida)

# Obtener dimensiones
height, width = arr.shape[:2]
window = pygame.display.set_mode((width * 2, height))
pygame.display.set_caption('Imagen Original e Invertida')

# Mostrar ambas imágenes lado a lado
window.blit(surface_original, (0, 0))
window.blit(surface_invertida, (width, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()