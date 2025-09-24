import pygame
import sys

def rgb_to_grayscale_weighted(rgb):
    r, g, b = rgb
    # Fórmula ponderada: 0.299*R + 0.587*G + 0.114*B
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return (gray, gray, gray)

def convert_surface_to_grayscale(surface):
    width, height = surface.get_size()
    grayscale_surface = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            color = surface.get_at((x, y))
            gray = rgb_to_grayscale_weighted(color[:3])
            grayscale_surface.set_at((x, y), gray)
    return grayscale_surface

def main():
    pygame.init()
    image_path = "pruebaimagen.jpeg"
    try:
        original = pygame.image.load(image_path)
    except pygame.error:
        print(f"No se pudo cargar la imagen: {image_path}")
        sys.exit(1)

    grayscale = convert_surface_to_grayscale(original)

    width, height = original.get_size()
    window = pygame.display.set_mode((width * 2, height))
    pygame.display.set_caption("Original y Escala de Grises")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((0, 0, 0))
        window.blit(original, (0, 0))
        window.blit(grayscale, (width, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()