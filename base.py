from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        #  НАЧАЛО ИГРЫ -> None
        #  присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        #  а также выставляем True для свойства "началась ли игра"
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        #  ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        #  проверка здоровья игрока и врага и возвращение результата строкой:
        #  может быть три результата:
        #  Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        #  если Здоровья игроков в порядке то ничего не происходит
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.player.hp = 0 # делаем ноль для красивого вывода
            self.enemy.hp = 0
            self.battle_result = 'Ничья'
            return self.battle_result
        if self.player.hp <= 0:
            self.player.hp = 0
            self.battle_result = 'Игрок проиграл битву'
            return self.battle_result
        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.battle_result = 'Игрок выиграл битву'
            return self.battle_result

    def _stamina_regeneration(self):
        #  регенерация здоровья и стамины для игрока и врага за ход
        #  в этом методе к количеству стамины игрока и врага прибавляется константное значение.
        #  главное чтобы оно не привысило максимальные значения (используйте if)
        self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina

        self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self) -> str:
        #  СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        #  срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        #  создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        #  если result -> возвращаем его
        #  если же результата пока нет и после завершения хода игра продолжается,
        #  тогда запускаем процесс регенерации стамины и здоровья для игроков (self._stamina_regeneration)
        #  и вызываем функцию self.enemy.hit(self.player) - ответный удар врага
        result = self._check_players_hp()
        if result:
            return result

        enemy_hit_result = self.enemy.hit(self.player)
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return enemy_hit_result

    def _end_game(self):
        #  КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        #  очищаем синглтон - self._instances = {}
        #  останавливаем игру (game_is_running)
        #  возвращаем результат
        self._instances = {}
        self.game_is_running = False
        return 'Досрочное завершение'

    def player_hit(self) -> str:
        #  КНОПКА УДАР ИГРОКА -> return result: str
        #  получаем результат от функции self.player.hit
        #  запускаем следующий ход
        #  возвращаем результат удара строкой
        result = self.player.hit(self.enemy)
        return result

    def player_use_skill(self) -> str:
        #  КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        #  получаем результат от функции self.use_skill
        #  включаем следующий ход
        #  возвращаем результат удара строкой
        result = self.player.use_skill(self.enemy)
        return result
