import matplotlib.pyplot as plt
from skimage import io, img_as_float, img_as_ubyte
import numpy as np

imagen = io.imread("foto.jfif")
imagen_float = img_as_float(imagen)

# Definir kernel de blur 3x3
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])

imagen_blur = np.zeros_like(imagen_float)


for c in range(3): 
    for i in range(1, imagen_float.shape[0]-1):
        for j in range(1, imagen_float.shape[1]-1):
            region = imagen_float[i-1:i+2, j-1:j+2, c] 
            imagen_blur[i, j, c] = np.sum(region * kernel) 

imagen_blur_uint8 = img_as_ubyte(imagen_blur)

# Mostrar resultados
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(imagen)
axes[0].set_title("Imagen Original")
axes[0].axis("off")

axes[1].imshow(imagen_blur_uint8)
axes[1].set_title("Imagen con Blur 3x3")
axes[1].axis("off")

plt.show()

