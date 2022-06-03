from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from classes import UnitClass
from equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon
        self.armor = Armor
        self._is_skill_used = False

    @property
    def health_points(self):
        #  возвращаем аттрибут hp в красивом виде
        return f'{round(self.hp, 1)}'

    @property
    def stamina_points(self):
        #  возвращаем аттрибут stamina в красивом виде
        return f'{round(self.stamina, 1)}'

    def equip_weapon(self, weapon: Weapon):
        #  присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        #  одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        #  Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        attacker_damage = self.weapon.damage * self.unit_class.attack
        target_armor = 0
        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina = target.stamina - target.armor.stamina_per_turn
            target_armor = target.armor.defence * target.unit_class.armor
        damage = attacker_damage - target_armor
        target.get_damage(damage)
        return round(damage, 1)

    def get_damage(self, damage: [int, float]) -> Optional[int]:
        #  получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        self.hp = self.hp - damage
        return damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return 'Навык уже использован'
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina >= self.weapon.stamina_per_hit:
            self.stamina -= self.weapon.stamina_per_hit
            damage = self._count_damage(target)
            if damage <= 0:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        #  результат функции должен возвращать результат функции skill.use или же следующие строки:
        option = randint(1, 100)
        if option <= 10 and not self._is_skill_used:
            return self.use_skill(target)
        if self.stamina >= self.weapon.stamina_per_hit:
            self.stamina -= self.weapon.stamina_per_hit
            damage = self._count_damage(target)
            if damage <= 0:
                return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
