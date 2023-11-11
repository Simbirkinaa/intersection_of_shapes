import unittest
from main import *

class TestOpenGLFunctions(unittest.TestCase):

    def setUp(self):
        # Инициализация glfw и создание окна
        if not glfw.init():
            self.fail("glfw initialization failed")

        self.window = glfw.create_window(1, 1, "Test Window", None, None)
        if not self.window:
            glfw.terminate()
            self.fail("glfw window creation failed")

        glfw.make_context_current(self.window)

    def tearDown(self):
        # Завершение glfw
        glfw.terminate()

    def test_draw_tetrahedron(self):
        # Проверяем, что функция успешно отрисовывает тетраэдр
        # Мы не можем напрямую сравнить изображения, поэтому просто проверим, что
        # функция завершается без ошибок (не вызывает исключений).
        try:
            draw_tetrahedron()
        except Exception as e:
            self.fail(f"draw_tetrahedron() raised an exception: {e}")

    def test_draw_cylinder(self):
        # Проверяем, что функция успешно отрисовывает цилиндр
        # Мы не можем напрямую сравнить изображения, поэтому просто проверим, что
        # функция завершается без ошибок (не вызывает исключений).
        try:
            draw_cylinder()
        except Exception as e:
            self.fail(f"draw_cylinder() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
