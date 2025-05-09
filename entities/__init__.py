"""
Базовый модуль для игровых сущностей (Entity-Component-System подход)
"""

from abc import ABC, abstractmethod
import pygame


class Entity(ABC):
    """
    Абстрактный базовый класс для всех игровых сущностей
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.components = []
        self.active = True
        self.tag = ""  # Для идентификации сущности

    def add_component(self, component):
        """Добавляет компонент к сущности"""
        self.components.append(component)
        component.entity = self
        return component

    def get_component(self, component_type):
        """Возвращает первый компонент указанного типа"""
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, delta_time):
        """Обновляет все компоненты сущности"""
        if not self.active:
            return

        for component in self.components:
            component.update(delta_time)

    def render(self, surface):
        """Отрисовывает все компоненты сущности"""
        if not self.active:
            return

        for component in self.components:
            component.render(surface)

    def destroy(self):
        """Помечает сущность для удаления"""
        self.active = False

    @abstractmethod
    def on_collision(self, other):
        """Обработка столкновений с другой сущностью"""
        pass


class Component(ABC):
    """
    Базовый класс для компонентов, которые можно добавлять к сущностям
    """

    def __init__(self):
        self.entity = None  # Родительская сущность

    def update(self, delta_time):
        """Логика обновления компонента"""
        pass

    def render(self, surface):
        """Отрисовка компонента"""
        pass


class Transform(Component):
    """
    Компонент трансформации (положение, вращение, масштаб)
    """

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.rotation = 0
        self.scale = 1.0

    def get_position(self):
        return (self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y


class SpriteRenderer(Component):
    """
    Компонент для отрисовки спрайтов
    """

    def __init__(self, sprite=None, color=(255, 255, 255), size=(32, 32)):
        super().__init__()
        self.sprite = sprite
        self.color = color
        self.size = size

        if self.sprite is None:
            # Создаем простой прямоугольник, если спрайт не задан
            self.sprite = pygame.Surface(size)
            self.sprite.fill(color)

    def render(self, surface):
        if self.entity and self.sprite:
            transform = self.entity.get_component(Transform)
            if transform:
                surface.blit(self.sprite, (transform.x, transform.y))


class Collider(Component):
    """
    Базовый компонент для обработки столкновений
    """

    def __init__(self, width=32, height=32):
        super().__init__()
        self.width = width
        self.height = height
        self.is_trigger = False  # Если True, не блокирует движение

    def get_rect(self):
        """Возвращает прямоугольник столкновений"""
        if self.entity:
            transform = self.entity.get_component(Transform)
            if transform:
                return pygame.Rect(transform.x, transform.y, self.width, self.height)
        return pygame.Rect(0, 0, self.width, self.height)

    def check_collision(self, other_collider):
        """Проверяет столкновение с другим коллайдером"""
        return self.get_rect().colliderect(other_collider.get_rect())


# Фабрика сущностей для удобного создания
class EntityFactory:
    @staticmethod
    def create_player(x, y):
        """Создает сущность игрока с базовыми компонентами"""
        player = Entity(x, y)
        player.tag = "Player"

        player.add_component(Transform(x, y))
        player.add_component(SpriteRenderer(color=(0, 0, 255), size=(32, 32)))
        player.add_component(Collider(32, 32))

        return player

    @staticmethod
    def create_enemy(x, y):
        """Создает сущность врага"""
        enemy = Entity(x, y)
        enemy.tag = "Enemy"

        enemy.add_component(Transform(x, y))
        enemy.add_component(SpriteRenderer(color=(255, 0, 0), size=(32, 32)))
        enemy.add_component(Collider(32, 32))

        return enemy