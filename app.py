from flask import Flask, render_template, request, redirect

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}
equipment = Equipment()

arena = Arena()  # инициализируем класс арены


@app.route("/")
def menu_page():
    #  рендерим главное меню (шаблон index.html)
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    #  выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    #  рендерим экран боя (шаблон fight.html)
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    #  кнопка нанесения удара
    #  обновляем экран боя (нанесение удара) (шаблон fight.html)
    #  если игра идет - вызываем метод player.hit() экземпляра класса арены
    #  если игра не идет - пропускаем срабатывание метода (просто рендерим шаблон с текущими данными)
    result = arena.player_hit()
    battle_result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
    #  кнопка использования скилла
    #  логика пркатикчески идентична предыдущему эндпоинту
    result = arena.player_use_skill()
    battle_result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    #  кнопка пропуск хода
    #  логика практически идентична предыдущему эндпоинту
    #  однако вызываем здесь функцию следующий ход (arena.next_turn())
    battle_result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, battle_result=battle_result)


@app.route("/fight/end-fight")
def end_fight():
    #  кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['get'])
def choose_hero_get():
    #  кнопка выбор героя. 2 метода GET и POST
    #  на GET отрисовываем форму.
    return render_template('hero_choosing.html', result={
        "header": 'Выбор Вашего персонажа',  # для названия страниц
        "classes": unit_classes.keys(),  # для названия классов
        "weapons": equipment.get_weapons_names(),  # для названия оружия
        "armors": equipment.get_armors_names()  # для названия брони
    })


@app.route("/choose-hero/", methods=['post'])
def choose_hero_post():
    #  на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    name = request.form.get('name')
    unit_class_name = request.form.get('unit_class')
    unit_class = unit_classes[unit_class_name]

    weapon_name = request.form.get('weapon')
    weapon = equipment.get_weapon(weapon_name)

    armor_name = request.form.get('armor')
    armor = equipment.get_armor(armor_name)

    player = PlayerUnit(name, unit_class)
    player.equip_weapon(weapon)
    player.equip_armor(armor)
    heroes['player'] = player
    return redirect('/choose-enemy/', code=302)


@app.route("/choose-enemy/", methods=['get'])
def choose_enemy_get():
    #  кнопка выбор соперников. 2 метода GET и POST
    #  на GET отрисовываем форму.
    return render_template('hero_choosing.html', result={
        "header": 'Выбор противника',  # для названия страниц
        "classes": unit_classes.keys(),  # для названия классов
        "weapons": equipment.get_weapons_names(),  # для названия оружия
        "armors": equipment.get_armors_names()  # для названия брони
    })


@app.route("/choose-enemy/", methods=['post'])
def choose_enemy_post():
    #  кнопка выбор соперников. 2 метода GET и POST
    #  а на POST отправляем форму и делаем редирект на начало битвы
    name = request.form.get('name')
    unit_class_name = request.form.get('unit_class')
    unit_class = unit_classes[unit_class_name]

    weapon_name = request.form.get('weapon')
    weapon = equipment.get_weapon(weapon_name)

    armor_name = request.form.get('armor')
    armor = equipment.get_armor(armor_name)

    enemy = EnemyUnit(name, unit_class)
    enemy.equip_weapon(weapon)
    enemy.equip_armor(armor)
    heroes['enemy'] = enemy
    return redirect('/fight/', code=302)


if __name__ == "__main__":
    app.run()
