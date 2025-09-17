import matplotlib.pyplot as plt
from skimage import io

imagen = io.imread("foto.jfif")

# Separar los canales
R = imagen[:, :, 0]  
G = imagen[:, :, 1]   
B = imagen[:, :, 2]   

# Mostrar resultados
fig, axes = plt.subplots(1, 4, figsize=(15, 5))

axes[0].imshow(imagen)
axes[0].set_title("Imagen Original")
axes[0].axis("off")

axes[1].imshow(R, cmap="Reds")
axes[1].set_title("Canal Rojo")
axes[1].axis("off")

axes[2].imshow(G, cmap="Greens")
axes[2].set_title("Canal Verde")
axes[2].axis("off")

axes[3].imshow(B, cmap="Blues")
axes[3].set_title("Canal Azul")
axes[3].axis("off")

plt.show()
