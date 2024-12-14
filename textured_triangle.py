import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_texture():
    # Load a texture using pygame
    texture_surface = pygame.image.load("texture.jpg")  # Replace with your texture file path
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    # Generate a texture ID and bind it
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Upload texture data to GPU
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def draw_textured_triangle():
    glEnable(GL_TEXTURE_2D)  # Enable texturing

    glBegin(GL_TRIANGLES)

    # Bottom-left vertex
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-0.5, -0.5, 0.0)

    # Bottom-right vertex
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0.5, -0.5, 0.0)

    # Top vertex
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 0.5, 0.0)

    glEnd()

    glDisable(GL_TEXTURE_2D)  # Disable texturing

def main():
    pygame.init()

    # Set up the display using pygame
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Textured OpenGL Triangle with Pygame")

    # Initialize OpenGL viewport and projection
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -2.0)  # Move the triangle into view

    angle = 0  # Initialize rotation angle
    clock = pygame.time.Clock()  # Initialize pygame clock for delta time calculation

    # Load the texture
    texture_id = load_texture()

    # Main loop
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Calculate delta time in seconds

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply rotation
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -2.0)
        glRotatef(angle, 0, 1, 0)  # Rotate around the Y-axis

        # Bind the texture and draw the triangle
        glBindTexture(GL_TEXTURE_2D, texture_id)
        draw_textured_triangle()

        # Update the angle for the next frame using delta time
        angle += 90 * delta_time  # Rotate 90 degrees per second

        # Swap buffers to display the rendered image
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
