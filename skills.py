from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            user._is_skill_used = True
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = 'Свирепый пинок'
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        #  логика использования скилла -> return str
        #  в классе нам доступны экземпляры user и target - можно использовать любые их методы
        #  именно здесь происходит уменьшение стамины у игрока применяющего умение и
        #  уменьшение здоровья цели.
        #  результат применения возвращаем строкой
        self.user.stamina -= self.stamina
        damage_count = self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {damage_count} урона сопернику.'


class HardShot(Skill):
    name = 'Мощный укол'
    stamina = 5
    damage = 15

    def skill_effect(self):
        self.user.stamina -= self.stamina
        damage_count = self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {damage_count} урона сопернику.'
