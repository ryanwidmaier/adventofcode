import math
import itertools


player = {'hp': 100, 'dmg': 0, 'amr': 0}
boss = {'hp': 103, 'dmg': 9, 'amr': 2}


def player_win(player, boss):
    player_dmg = max(1, player['dmg'] - boss['amr'])
    boss_dmg = max(1, boss['dmg'] - player['amr'])

    player_wins_in = math.ceil(boss['hp'] / player_dmg)
    boss_wins_in = math.ceil(player['hp'] / boss_dmg)

    return player_wins_in <= boss_wins_in


# sample = player_win(
#     {'hp': 8, 'dmg': 5, 'amr': 5},
#     {'hp': 12, 'dmg': 7, 'amr': 2},
# )
# print(sample)

weapons = [
    ('dagger',      8, 4, 0),
    ('shortsword', 10, 5, 0),
    ('warhammer',  25, 6, 0),
    ('longsword',  40, 7, 0),
    ('greataxe',   74, 8, 0),
]
armors = [
    ('none',         0, 0, 0),
    ('leather',     13, 0, 1),
    ('chainmail',   31, 0, 2),
    ('splintmail',  53, 0, 3),
    ('bandedmail',  75, 0, 4),
    ('platemail',  102, 0, 5),
]
all_rings = [
    ('d+1',  25, 1, 0),
    ('d+2',  50, 2, 0),
    ('d+3', 100, 3, 0),
    ('a+1',  20, 0, 1),
    ('a+2',  40, 0, 2),
    ('a+3',  80, 0, 3),
]

min_cost = 99999999999999999
max_cost = 0
for weapon in weapons:
    for armor in armors:
        for num_rings in range(3):
            for rings in itertools.combinations(all_rings, num_rings):
                items = [weapon, armor] + list(rings)
                player = {
                    'hp': 100,
                    'cost': sum(it[1] for it in items),
                    'dmg': sum(it[2] for it in items),
                    'amr': sum(it[3] for it in items),
                }
                if player_win(player, boss):
                    min_cost = min(min_cost, player['cost'])
                if not player_win(player, boss):
                    max_cost = max(max_cost, player['cost'])
                    if max_cost == 206:
                        player_win(player, boss)

print(min_cost)
print(max_cost)
