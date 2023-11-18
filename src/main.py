import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Параметры тетраэдра
tetrahedron_vertices = [
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0, 0.5, -0.5),
    (0, 0, 0.5)
]
tetrahedron_faces = [
    (0, 1, 2),
    (0, 1, 3),
    (1, 2, 3),
    (2, 0, 3)
]

# Параметры цилиндра
cylinder_radius = 0.25  # Уменьшенный радиус
cylinder_height = 0.5
cylinder_slices = 30
# Углы для вращения
x = 0
y = 0
z = 0
"""
     Функция draw_tetrahedron() отрисовывает тетраэдр в окне OpenGL с использованием смешивания цветов.
     Цвет устанавливается с помощью glColor4f(), где первые 3 значения задают  цвет, 
     последнее устанавливает прозрачность на половину (50%). Для удобства значения координат 
     каждой вершины были умножены на 0.5 для изменения размера тетраэдра.
"""
def draw_tetrahedron():
    glEnable(GL_BLEND)  # смешивание цветов
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 0.0, 0.0, 0.5)  # Цвет тетраэдра
    for face in tetrahedron_faces:
        for vertex_index in face:
            glVertex3fv([coord * 0.5 for coord in tetrahedron_vertices[vertex_index]])
    glEnd()

"""
     Функция draw_cylinder() предназначена для отрисовки цилиндра в окне OpenGL.
     В функции создается объект quadric, который используется для отрисовки 
     геометрических примитивов в OpenGL. glColor4f() устанавливает цвет цилиндра. 
     Цилиндр отрисовывается с использованием заданных параметров (радиус, высота, количество сегментов).
"""
def draw_cylinder():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    glColor4f(0.0, 0.0, 1.0, 0.5)
    gluCylinder(quadric, cylinder_radius, cylinder_radius, cylinder_height, cylinder_slices, 1)
    # Основание в начале цилиндра
    glPushMatrix()
    glTranslatef(0, 0, cylinder_height / 2)
    gluDisk(quadric, 0, cylinder_radius, cylinder_slices, 1)
    glPopMatrix()
    # Основание в конце цилиндра
    glPushMatrix()
    glTranslatef(0, 0, cylinder_height)
    gluDisk(quadric, 0, cylinder_radius, cylinder_slices, 1)
    glPopMatrix()
    glDisable(GL_BLEND)

"""
     Функция display() используется для отображения графики в окне OpenGL.
     Эта функция отрисовывает тетраэдр и цилиндр в соответствии с установленными 
     углами вращения и цветами для каждой из фигур. С помощью glRotatef() происходит
     поворот сцены вокруг осей на определенный угол.
"""
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    glRotatef(z, 0, 0, 1)

    glColor3f(1.0, 0.0, 0.0)  # Цвет тетраэдра
    draw_tetrahedron()

    glColor3f(0.0, 0.0, 1.0)  # Цвет цилиндра
    glTranslatef(0, 0, -cylinder_height / 2)
    draw_cylinder()

    glfw.swap_buffers(window)

"""
    Функция key_callback() отвечает за обработку событий клавиатуры в окне OpenGL.
    Она позволяет управлять поворотом сцены с помощью стрелок на клавиатуре,
    а также клавиш "Z" и "X" для поворота вокруг оси Z.
"""
def key_callback(_, key, __, action, ___):
    global x, y, z

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            x += 5
        elif key == glfw.KEY_DOWN:
            x -= 5
        elif key == glfw.KEY_LEFT:
            y -= 5
        elif key == glfw.KEY_RIGHT:
            y += 5
        elif key == glfw.KEY_Z:
            z += 5
        elif key == glfw.KEY_X:
            z -= 5

def main():
    global window
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Intersection of Tetrahedron and Cylinder", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0, 0, -5)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        display()

    glfw.terminate()

if __name__ == "__main__":
    main()