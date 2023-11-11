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

# Функция draw_tetrahedron() отрисовывает тетраэдр в окне OpenGL с использованием смешивания цветов.
# Внутри используется glBegin(GL_TRIANGLES) для начала определения треугольников, которые будут отображаться.
# Далее устанавливается цвет с помощью glColor4f, где первые три значения задают  цвет, последнее устанавливает
# прозрачность на половину (50%). Далее функция проходит по каждой грани тетраэдра.
# Для каждого индекса вершины в грани вычисляются соответствующие координаты вершины из списка tetrahedron_vertices.
# Значения координат каждой вершины умножаются на 0.5 для изменения размера тетраэдра.
def draw_tetrahedron():
    glEnable(GL_BLEND)  # смешивание цветов
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # параметры смешивания
    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 0.0, 0.0, 0.5)  # Цвет тетраэдра (красный)
    for face in tetrahedron_faces:
        for vertex_index in face:
            glVertex3fv([coord * 0.5 for coord in tetrahedron_vertices[vertex_index]])
    glEnd()

# функция draw_cylinder() отрисовывает цилиндр в окне OpenGL с использованием смешивания цветов и полупрозрачности.
# glEnable(GL_BLEND) включает смешивание цветов.
# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) устанавливает параметры смешивания.
# Далее создается объект quadric, который используется для отрисовки геометрических примитивов в OpenGL.
# gluQuadricTexture(quadric, GL_TRUE) позволяет применять текстуры к отрисовываемым примитивам.
# glColor4f устанавливает цвет цилиндра. Первые три значения задают синий цвет, последнее значение - прозрачность (50%).
# Затем отрисовывается цилиндр с использованием заданных параметров (радиус, высота, количество сегментов).
# glTranslatef выполняет сдвиг вдоль оси z, чтобы переместиться к началу цилиндра.
# gluDisk отрисовывает основания цилиндра.
def draw_cylinder():
    glEnable(GL_BLEND)  # Включаем смешивание цветов
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Устанавливаем параметры смешивания
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    glColor4f(0.0, 0.0, 1.0, 0.5)  # Синий цвет с полупрозрачностью
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
# функция display() отображает содержимое окна OpenGL.
# glClear очищает буферы цвета и глубины, чтобы очистить предыдущие отрисованные кадры.
# glLoadIdentity() восстанавливает начальное положение и ориентацию камеры.
# glRotatef(x, 1, 0, 0) поворачивает сцену вокруг оси X на угол x.
# glRotatef(y, 0, 1, 0): Поворачивает сцену вокруг оси Y на угол y.
# glRotatef(z, 0, 0, 1): Поворачивает сцену вокруг оси Z на угол z.
# glColor3f устанавливает цвет тетраэдра.
# draw_tetrahedron() отрисовывает тетраэдр с использованием текущего установленного цвета.
# glColor3f устанавливает цвет цилиндра на синий.
# glTranslatef(0, 0, -cylinder_height / 2) выполняет сдвиг вдоль оси Z, чтобы переместиться к положению цилиндра.
# draw_cylinder() отрисовывает цилиндр с использованием текущего цвета.
# glfw.swap_buffers(window) обновляет содержимое окна, переключая буферы, чтобы отобразить новый кадр.
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    glRotatef(z, 0, 0, 1)

    glColor3f(1.0, 0.0, 0.0)  # Цвет тетраэдра (красный)
    draw_tetrahedron()

    glColor3f(0.0, 0.0, 1.0)  # Цвет цилиндра (синий)
    glTranslatef(0, 0, -cylinder_height / 2)
    draw_cylinder()

    glfw.swap_buffers(window)

# функция key_callback() отвечает за обработку событий клавиатуры в окне OpenGL.
# Она позволяет управлять поворотом сцены с помощью стрелок на клавиатуре,
# а также клавиш "Z" и "X" для поворота вокруг оси Z. Изменения сохраняются в переменных
# x, y, z, которые используются в функции display() для отображения сцены с учетом поворотов.
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
