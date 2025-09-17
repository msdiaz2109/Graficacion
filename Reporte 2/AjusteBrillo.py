import matplotlib.pyplot as plt
from skimage import io, img_as_float, img_as_ubyte
import numpy as np

imagen = io.imread("foto.jfif")
imagen_float = img_as_float(imagen)

factor = float(input("Introduce un valor de brillo (-1 a 1): "))

# Ajuste de brillo
imagen_brillo = imagen_float + factor
imagen_brillo = np.clip(imagen_brillo, 0, 1)
imagen_brillo_uint8 = img_as_ubyte(imagen_brillo)

# Mostrar resultados
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(imagen)
axes[0].set_title("Imagen Original")
axes[0].axis("off")

axes[1].imshow(imagen_brillo_uint8)
axes[1].set_title(f"Imagen con brillo {factor}")
axes[1].axis("off")

plt.show()
