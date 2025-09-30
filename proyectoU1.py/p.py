import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import numpy as np
import math
import os
from datetime import datetime
from PIL import Image

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
herramientas_dibujo = ["línea", "rectángulo", "círculo", "polígono"]
herramientas_edicion = ["seleccionar", "borrador"]

colores = ["Negro", "Rojo", "Verde", "Azul", "Rosa", "Celeste"]
color_actual = colores[0]

figuras = []
lineas = []
puntos_poligono = []
seleccionado = None
inicio = None
linea_temporal = None

# =============================================================================
# CONFIGURACIÓN DE LA INTERFAZ
# =============================================================================
fig, ax = plt.subplots(figsize=(13, 8))
plt.subplots_adjust(bottom=0.25, top=0.95)
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)
ax.set_aspect("equal")
ax.set_facecolor('#f8f9fa')
ax.grid(True, linestyle='--', alpha=0.3)

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================
def actualizar_titulo():
    herramienta = herramienta_actual
    color = color_actual
    sel = "Sí" if seleccionado else "No"
    ax.set_title(f"Editor de Dibujo | Herramienta: {herramienta} | Color: {color} | Selección: {sel}", 
                fontsize=12, pad=10, fontweight='bold')
    fig.canvas.draw_idle()

def guardar_imagen(evento):
    try:
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"dibujo_{fecha_hora}.bmp"
        print("Procesando guardado de imagen...")
        png_temporal = f"temp_{fecha_hora}.png"
        plt.savefig(png_temporal, format='png', dpi=150, bbox_inches='tight', 
                   pad_inches=0.1, facecolor='white', edgecolor='none')
        with Image.open(png_temporal) as img:
            img.save(nombre_archivo, 'BMP')
        if os.path.exists(png_temporal):
            os.remove(png_temporal)
        ax.set_title(f"✓ GUARDADO: {nombre_archivo}", fontsize=12, pad=10, color='green')
        fig.canvas.draw_idle()
        plt.pause(1.5)
        actualizar_titulo()
    except Exception as e:
        print(f"ERROR al guardar: {e}")
        ax.set_title("✗ ERROR al guardar", fontsize=12, pad=10, color='red')
        fig.canvas.draw_idle()
        plt.pause(1.5)
        actualizar_titulo()

def obtener_color_matplotlib(color_espanol):
    mapeo_colores = {
        "Negro": "black",
        "Rojo": "red", 
        "Verde": "green",
        "Azul": "blue",
        "Rosa": "magenta",
        "Celeste": "cyan"
    }
    return mapeo_colores.get(color_espanol, "black")

def encontrar_figura_en_punto(x, y):
    if x is None or y is None:
        return None
    tolerancia = 10
    todas_figuras = lineas + figuras
    for figura in reversed(todas_figuras):
        if isinstance(figura, Line2D):
            datos_x, datos_y = figura.get_data()
            if len(datos_x) == 2:
                x1, y1 = datos_x[0], datos_y[0]
                x2, y2 = datos_x[1], datos_y[1]
                longitud_linea = math.hypot(x2 - x1, y2 - y1)
                if longitud_linea > 0:
                    t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (longitud_linea ** 2)
                    t = max(0, min(1, t))
                    proj_x = x1 + t * (x2 - x1)
                    proj_y = y1 + t * (y2 - y1)
                    dist = math.hypot(x - proj_x, y - proj_y)
                    if dist <= tolerancia:
                        return figura
        elif isinstance(figura, Circle):
            cx, cy = figura.center
            dist = math.hypot(x - cx, y - cy)
            if dist <= figura.radius:
                return figura
        elif isinstance(figura, Rectangle):
            x_rect, y_rect = figura.get_xy()
            ancho = figura.get_width()
            alto = figura.get_height()
            if (x_rect <= x <= x_rect + ancho and y_rect <= y <= y_rect + alto):
                return figura
        elif isinstance(figura, Polygon):
            vertices = figura.get_xy()
            for i in range(len(vertices) - 1):
                x1, y1 = vertices[i]
                x2, y2 = vertices[i + 1]
                longitud_linea = math.hypot(x2 - x1, y2 - y1)
                if longitud_linea > 0:
                    t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (longitud_linea ** 2)
                    t = max(0, min(1, t))
                    proj_x = x1 + t * (x2 - x1)
                    proj_y = y1 + t * (y2 - y1)
                    dist = math.hypot(x - proj_x, y - proj_y)
                    if dist <= tolerancia:
                        return figura
    return None

def seleccionar_figura(x, y):
    global seleccionado, color_figura_original
    if seleccionado:
        color_original = obtener_color_matplotlib(color_figura_original)
        if isinstance(seleccionado, Line2D):
            seleccionado.set_color(color_original)
            seleccionado.set_linestyle('-')
            seleccionado.set_linewidth(1)
        else:
            seleccionado.set_edgecolor(color_original)
            seleccionado.set_linestyle('-')
            seleccionado.set_linewidth(1)
    encontrada = encontrar_figura_en_punto(x, y)
    seleccionado = encontrada
    if seleccionado:
        color_figura_original = color_actual
        if isinstance(seleccionado, Line2D):
            seleccionado.set_color('orange')
            seleccionado.set_linestyle('--')
            seleccionado.set_linewidth(2)
        else:
            seleccionado.set_edgecolor('orange')
            seleccionado.set_linestyle('--')
            seleccionado.set_linewidth(2)
    fig.canvas.draw_idle()
    actualizar_titulo()

# =============================================================================
# FUNCIONES DE ROTACIÓN Y REDIMENSIONAMIENTO
# =============================================================================
def rotar_figura(evento):
    global seleccionado
    if seleccionado is None:
        ax.set_title("Selecciona una figura primero", fontsize=12, pad=10, color='orange')
        fig.canvas.draw_idle()
        plt.pause(1)
        actualizar_titulo()
        return
    try:
        if isinstance(seleccionado, Line2D):
            datos_x, datos_y = seleccionado.get_data()
            if len(datos_x) == 2:
                x1, y1 = datos_x[0], datos_y[0]
                x2, y2 = datos_x[1], datos_y[1]
                centro_x = (x1 + x2) / 2
                centro_y = (y1 + y2) / 2
                angulo = math.radians(45)
                nuevo_x1 = centro_x + (x1 - centro_x) * math.cos(angulo) - (y1 - centro_y) * math.sin(angulo)
                nuevo_y1 = centro_y + (x1 - centro_x) * math.sin(angulo) + (y1 - centro_y) * math.cos(angulo)
                nuevo_x2 = centro_x + (x2 - centro_x) * math.cos(angulo) - (y2 - centro_y) * math.sin(angulo)
                nuevo_y2 = centro_y + (x2 - centro_x) * math.sin(angulo) + (y2 - centro_y) * math.cos(angulo)
                seleccionado.set_data([nuevo_x1, nuevo_x2], [nuevo_y1, nuevo_y2])
        elif isinstance(seleccionado, Rectangle):
            x, y = seleccionado.get_xy()
            ancho = seleccionado.get_width()
            alto = seleccionado.get_height()
            seleccionado.set_width(alto)
            seleccionado.set_height(ancho)
        elif isinstance(seleccionado, Circle):
            ax.set_title("Los círculos no se pueden rotar", fontsize=12, pad=10, color='orange')
            fig.canvas.draw_idle()
            plt.pause(1)
            actualizar_titulo()
            return
        elif isinstance(seleccionado, Polygon):
            vertices = seleccionado.get_xy()
            centro_x = np.mean(vertices[:, 0])
            centro_y = np.mean(vertices[:, 1])
            angulo = math.radians(45)
            nuevos_vertices = []
            for vertice in vertices:
                x, y = vertice
                nuevo_x = centro_x + (x - centro_x) * math.cos(angulo) - (y - centro_y) * math.sin(angulo)
                nuevo_y = centro_y + (x - centro_x) * math.sin(angulo) + (y - centro_y) * math.cos(angulo)
                nuevos_vertices.append([nuevo_x, nuevo_y])
            seleccionado.set_xy(nuevos_vertices)
        ax.set_title("↻ Figura rotada", fontsize=12, pad=10, color='blue')
        fig.canvas.draw_idle()
        plt.pause(0.5)
        actualizar_titulo()
    except Exception as e:
        print(f"ERROR al rotar figura: {e}")

def redimensionar_figura(evento):
    global seleccionado
    if seleccionado is None:
        ax.set_title("⚠️ Selecciona una figura primero", fontsize=12, pad=10, color='orange')
        fig.canvas.draw_idle()
        plt.pause(1)
        actualizar_titulo()
        return
    try:
        escala = 1.2
        if isinstance(seleccionado, Line2D):
            datos_x, datos_y = seleccionado.get_data()
            if len(datos_x) == 2:
                x1, y1 = datos_x[0], datos_y[0]
                x2, y2 = datos_x[1], datos_y[1]
                centro_x = (x1 + x2) / 2
                centro_y = (y1 + y2) / 2
                nuevo_x1 = centro_x + (x1 - centro_x) * escala
                nuevo_y1 = centro_y + (y1 - centro_y) * escala
                nuevo_x2 = centro_x + (x2 - centro_x) * escala
                nuevo_y2 = centro_y + (y2 - centro_y) * escala
                seleccionado.set_data([nuevo_x1, nuevo_x2], [nuevo_y1, nuevo_y2])
        elif isinstance(seleccionado, Rectangle):
            x, y = seleccionado.get_xy()
            ancho = seleccionado.get_width()
            alto = seleccionado.get_height()
            nuevo_ancho = ancho * escala
            nuevo_alto = alto * escala
            delta_ancho = (nuevo_ancho - ancho) / 2
            delta_alto = (nuevo_alto - alto) / 2
            seleccionado.set_width(nuevo_ancho)
            seleccionado.set_height(nuevo_alto)
            seleccionado.set_xy([x - delta_ancho, y - delta_alto])
        elif isinstance(seleccionado, Circle):
            radio_actual = seleccionado.get_radius()
            nuevo_radio = radio_actual * escala
            seleccionado.set_radius(nuevo_radio)
        elif isinstance(seleccionado, Polygon):
            vertices = seleccionado.get_xy()
            centro_x = np.mean(vertices[:, 0])
            centro_y = np.mean(vertices[:, 1])
            nuevos_vertices = []
            for vertice in vertices:
                x, y = vertice
                nuevo_x = centro_x + (x - centro_x) * escala
                nuevo_y = centro_y + (y - centro_y) * escala
                nuevos_vertices.append([nuevo_x, nuevo_y])
            seleccionado.set_xy(nuevos_vertices)
        ax.set_title("Figura agrandada +20%", fontsize=12, pad=10, color='blue')
        fig.canvas.draw_idle()
        plt.pause(0.5)
        actualizar_titulo()
    except Exception as e:
        print(f"ERROR al redimensionar figura: {e}")

def reducir_figura(evento):
    global seleccionado
    if seleccionado is None:
        ax.set_title("Selecciona una figura primero", fontsize=12, pad=10, color='orange')
        fig.canvas.draw_idle()
        plt.pause(1)
        actualizar_titulo()
        return
    try:
        escala = 0.8
        if isinstance(seleccionado, Line2D):
            datos_x, datos_y = seleccionado.get_data()
            if len(datos_x) == 2:
                x1, y1 = datos_x[0], datos_y[0]
                x2, y2 = datos_x[1], datos_y[1]
                centro_x = (x1 + x2) / 2
                centro_y = (y1 + y2) / 2
                nuevo_x1 = centro_x + (x1 - centro_x) * escala
                nuevo_y1 = centro_y + (y1 - centro_y) * escala
                nuevo_x2 = centro_x + (x2 - centro_x) * escala
                nuevo_y2 = centro_y + (y2 - centro_y) * escala
                seleccionado.set_data([nuevo_x1, nuevo_x2], [nuevo_y1, nuevo_y2])
        elif isinstance(seleccionado, Rectangle):
            x, y = seleccionado.get_xy()
            ancho = seleccionado.get_width()
            alto = seleccionado.get_height()
            nuevo_ancho = ancho * escala
            nuevo_alto = alto * escala
            delta_ancho = (nuevo_ancho - ancho) / 2
            delta_alto = (nuevo_alto - alto) / 2
            seleccionado.set_width(nuevo_ancho)
            seleccionado.set_height(nuevo_alto)
            seleccionado.set_xy([x - delta_ancho, y - delta_alto])
        elif isinstance(seleccionado, Circle):
            radio_actual = seleccionado.get_radius()
            nuevo_radio = radio_actual * escala
            seleccionado.set_radius(nuevo_radio)
        elif isinstance(seleccionado, Polygon):
            vertices = seleccionado.get_xy()
            centro_x = np.mean(vertices[:, 0])
            centro_y = np.mean(vertices[:, 1])
            nuevos_vertices = []
            for vertice in vertices:
                x, y = vertice
                nuevo_x = centro_x + (x - centro_x) * escala
                nuevo_y = centro_y + (y - centro_y) * escala
                nuevos_vertices.append([nuevo_x, nuevo_y])
            seleccionado.set_xy(nuevos_vertices)
        ax.set_title("Figura reducida -20%", fontsize=12, pad=10, color='blue')
        fig.canvas.draw_idle()
        plt.pause(0.5)
        actualizar_titulo()
    except Exception as e:
        print(f"ERROR al reducir figura: {e}")

# =============================================================================
# EVENTOS DE DIBUJO
# =============================================================================
def al_hacer_clic(evento):
    global inicio, puntos_poligono, seleccionado, linea_temporal
    if evento.inaxes != ax:
        return
    if herramienta_actual == "seleccionar":
        seleccionar_figura(evento.xdata, evento.ydata)
        return
    if herramienta_actual == "borrador":
        figura_a_borrar = encontrar_figura_en_punto(evento.xdata, evento.ydata)
        if figura_a_borrar:
            if figura_a_borrar == seleccionado:
                seleccionado = None
            if figura_a_borrar in lineas:
                lineas.remove(figura_a_borrar)
            elif figura_a_borrar in figuras:
                figuras.remove(figura_a_borrar)
            figura_a_borrar.remove()
            fig.canvas.draw_idle()
            actualizar_titulo()
        return
    if herramienta_actual in herramientas_dibujo:
        inicio = (evento.xdata, evento.ydata)
    if herramienta_actual == "polígono":
        puntos_poligono.append((evento.xdata, evento.ydata))
        if len(puntos_poligono) > 1:
            color_matplotlib = obtener_color_matplotlib(color_actual)
            ax.plot([puntos_poligono[-2][0], puntos_poligono[-1][0]],
                    [puntos_poligono[-2][1], puntos_poligono[-1][1]],
                    color=color_matplotlib, linewidth=2)
            fig.canvas.draw_idle()

def al_soltar_clic(evento):
    global inicio, seleccionado, linea_temporal
    if evento.inaxes != ax or inicio is None:
        return
    x0, y0 = inicio
    x1, y1 = evento.xdata, evento.ydata
    if linea_temporal:
        linea_temporal.remove()
        linea_temporal = None
    color_matplotlib = obtener_color_matplotlib(color_actual)
    if herramienta_actual == "línea":
        linea = Line2D([x0, x1], [y0, y1], color=color_matplotlib, linewidth=2)
        ax.add_line(linea)
        lineas.append(linea)
        seleccionado = linea
    elif herramienta_actual == "rectángulo":
        rect = Rectangle((min(x0, x1), min(y0, y1)), abs(x1 - x0), abs(y1 - y0),
                         fill=False, edgecolor=color_matplotlib, linewidth=2)
        ax.add_patch(rect)
        figuras.append(rect)
        seleccionado = rect
    elif herramienta_actual == "círculo":
        radio = math.hypot(x1 - x0, y1 - y0)
        circ = Circle((x0, y0), radio, fill=False, edgecolor=color_matplotlib, linewidth=2)
        ax.add_patch(circ)
        figuras.append(circ)
        seleccionado = circ
    inicio = None
    fig.canvas.draw_idle()
    actualizar_titulo()

def al_mover_mouse(evento):
    global linea_temporal, inicio
    if evento.inaxes != ax or inicio is None or herramienta_actual not in herramientas_dibujo:
        return
    x0, y0 = inicio
    x1, y1 = evento.xdata, evento.ydata
    if linea_temporal:
        linea_temporal.remove()
    color_matplotlib = obtener_color_matplotlib(color_actual)
    if herramienta_actual == "línea":
        linea_temporal = Line2D([x0, x1], [y0, y1], color=color_matplotlib, linestyle=':', alpha=0.7, linewidth=2)
        ax.add_line(linea_temporal)
    elif herramienta_actual == "rectángulo":
        ancho = abs(x1 - x0)
        alto = abs(y1 - y0)
        linea_temporal = Rectangle((min(x0, x1), min(y0, y1)), ancho, alto,
                                  fill=False, edgecolor=color_matplotlib, linestyle=':', alpha=0.7, linewidth=2)
        ax.add_patch(linea_temporal)
    elif herramienta_actual == "círculo":
        radio = math.hypot(x1 - x0, y1 - y0)
        linea_temporal = Circle((x0, y0), radio, fill=False, edgecolor=color_matplotlib, linestyle=':', alpha=0.7, linewidth=2)
        ax.add_patch(linea_temporal)
    fig.canvas.draw_idle()

# =============================================================================
# MANEJADORES DE BOTONES
# =============================================================================
def cambiar_herramienta_dibujo(evento):
    global indice_herramienta_dibujo, herramienta_actual, puntos_poligono
    indice_herramienta_dibujo = (indice_herramienta_dibujo + 1) % len(herramientas_dibujo)
    herramienta_actual = herramientas_dibujo[indice_herramienta_dibujo]
    if herramienta_actual != "polígono":
        puntos_poligono.clear()
    actualizar_titulo()

def establecer_seleccion(evento):
    global herramienta_actual, puntos_poligono
    herramienta_actual = "seleccionar"
    puntos_poligono.clear()
    actualizar_titulo()

def establecer_borrador(evento):
    global herramienta_actual, puntos_poligono
    herramienta_actual = "borrador"
    puntos_poligono.clear()
    actualizar_titulo()

def cambiar_color(evento):
    global indice_color, color_actual
    indice_color = (indice_color + 1) % len(colores)
    color_actual = colores[indice_color]
    if seleccionado:
        color_matplotlib = obtener_color_matplotlib(color_actual)
        if isinstance(seleccionado, Line2D):
            seleccionado.set_color(color_matplotlib)
        else:
            seleccionado.set_edgecolor(color_matplotlib)
    fig.canvas.draw_idle()
    actualizar_titulo()

def terminar_poligono(evento):
    global puntos_poligono, seleccionado
    if len(puntos_poligono) >= 3:
        color_matplotlib = obtener_color_matplotlib(color_actual)
        poligono = Polygon(puntos_poligono, fill=False, edgecolor=color_matplotlib, linewidth=2)
        ax.add_patch(poligono)
        figuras.append(poligono)
        seleccionado = poligono
        for i in range(len(puntos_poligono) - 1):
            if ax.lines:
                ax.lines[-1].remove()
        puntos_poligono.clear()
        fig.canvas.draw_idle()
        actualizar_titulo()
    elif len(puntos_poligono) > 0:
        for i in range(len(puntos_poligono) - 1):
            if ax.lines:
                ax.lines[-1].remove()
        puntos_poligono.clear()
        fig.canvas.draw_idle()

def limpiar_lienzo(evento):
    global figuras, lineas, seleccionado, puntos_poligono
    for figura in figuras:
        figura.remove()
    for linea in lineas:
        linea.remove()
    figuras.clear()
    lineas.clear()
    seleccionado = None
    puntos_poligono.clear()
    while ax.lines:
        ax.lines[0].remove()
    fig.canvas.draw_idle()
    actualizar_titulo()

# =============================================================================
# CONFIGURACIÓN DE BOTONES
# =============================================================================
ax_linea = plt.axes([0.02, 0.12, 0.10, 0.04])
ax_rectangulo = plt.axes([0.13, 0.12, 0.12, 0.04])
ax_circulo = plt.axes([0.26, 0.12, 0.10, 0.04])
ax_poligono = plt.axes([0.37, 0.12, 0.12, 0.04])

ax_seleccionar = plt.axes([0.02, 0.07, 0.12, 0.04])
ax_borrador = plt.axes([0.14, 0.07, 0.10, 0.04])
ax_color = plt.axes([0.25, 0.07, 0.12, 0.04])
ax_cerrar_poligono = plt.axes([0.38, 0.07, 0.12, 0.04])

ax_rotar = plt.axes([0.02, 0.02, 0.12, 0.04])
ax_agrandar = plt.axes([0.14, 0.02, 0.12, 0.04])
ax_reducir = plt.axes([0.26, 0.02, 0.12, 0.04])
ax_guardar = plt.axes([0.38, 0.02, 0.12, 0.04])
ax_limpiar = plt.axes([0.50, 0.02, 0.12, 0.04])

b_linea = Button(ax_linea, "Línea", color='#bbdefb')
b_rectangulo = Button(ax_rectangulo, "Rectángulo", color='#bbdefb')
b_circulo = Button(ax_circulo, "Círculo", color='#bbdefb')
b_poligono_btn = Button(ax_poligono, "Polígono", color='#bbdefb')

b_seleccionar = Button(ax_seleccionar, "Seleccionar", color='#c8e6c9')
b_borrador = Button(ax_borrador, "Borrador", color='#ffcdd2')
b_color = Button(ax_color, "Color", color='#fff9c4')  # Solo dice Color
b_cerrar_poligono = Button(ax_cerrar_poligono, "Cerrar Polígono", color='#c8e6c9')

b_rotar = Button(ax_rotar, "Rotar", color='#fff3e0')
b_agrandar = Button(ax_agrandar, "+20%", color='#e1f5fe')
b_reducir = Button(ax_reducir, "-20%", color='#f3e5f5')
b_guardar = Button(ax_guardar, "Guardar", color='#e8f5e8')
b_limpiar = Button(ax_limpiar, "Limpiar", color='#ffebee')

b_linea.on_clicked(lambda x: [globals().__setitem__('herramienta_actual', 'línea'), actualizar_titulo()])
b_rectangulo.on_clicked(lambda x: [globals().__setitem__('herramienta_actual', 'rectángulo'), actualizar_titulo()])
b_circulo.on_clicked(lambda x: [globals().__setitem__('herramienta_actual', 'círculo'), actualizar_titulo()])
b_poligono_btn.on_clicked(lambda x: [globals().__setitem__('herramienta_actual', 'polígono'), actualizar_titulo()])

b_seleccionar.on_clicked(establecer_seleccion)
b_borrador.on_clicked(establecer_borrador)
b_color.on_clicked(cambiar_color)
b_cerrar_poligono.on_clicked(terminar_poligono)

b_rotar.on_clicked(rotar_figura)
b_agrandar.on_clicked(redimensionar_figura)
b_reducir.on_clicked(reducir_figura)
b_guardar.on_clicked(guardar_imagen)
b_limpiar.on_clicked(limpiar_lienzo)

# =============================================================================
# VARIABLES GLOBALES Y CONFIGURACIÓN FINAL
# =============================================================================
indice_herramienta_dibujo = 0
herramienta_actual = herramientas_dibujo[indice_herramienta_dibujo]
indice_color = 0
color_actual = colores[indice_color]
color_figura_original = color_actual

fig.canvas.mpl_connect("button_press_event", al_hacer_clic)
fig.canvas.mpl_connect("button_release_event", al_soltar_clic)
fig.canvas.mpl_connect("motion_notify_event", al_mover_mouse)

actualizar_titulo()
plt.show()
