from collections import deque


def parse(lines):
    p1_lines, p2_lines = lines.lstrip('Player 1:\n').split('\nPlayer 2:\n')
    p1_lines = [int(x) for x in p1_lines.split()]
    p2_lines = [int(x) for x in p2_lines.split()]

    player1 = deque(p1_lines)
    player2 = deque(p2_lines)
    return player1, player2


def part1(player1, player2):
    round = 1
    while len(player1) > 0 and len(player2) > 0:
        print()
        print(f'-- Round {round} --')
        print(f"Player 1's deck: " + ', '.join(str(c) for c in player1))
        print(f"Player 2's deck: " + ', '.join(str(c) for c in player2))

        p1_card = player1.popleft()
        p2_card = player2.popleft()
        print(f'Player 1 plays: {p1_card}')
        print(f'Player 2 plays: {p2_card}')

        if p1_card > p2_card:
            print(f'Player 1 wins the round!')
            player1.append(p1_card)
            player1.append(p2_card)
        elif p2_card > p1_card:
            print(f'Player 2 wins the round!')
            player2.append(p2_card)
            player2.append(p1_card)

        round += 1

    winner = list(player1 if len(player1) else player2)
    winner.reverse()
    answer = sum((mult+1) * c for mult, c in enumerate(winner))
    print(f"Part 1: {answer}")


def part2(player1, player2):
    winner_num = play_game(1, player1, player2)
    print('== Post-game results ==')
    print(f"Player 1's deck: " + ', '.join(str(c) for c in player1))
    print(f"Player 2's deck: " + ', '.join(str(c) for c in player2))

    winner = list(player1 if winner_num == 1 else player2)
    winner.reverse()
    answer = sum((mult+1) * c for mult, c in enumerate(winner))
    print(f"Part 2: {answer}")


def play_game(game_num: int, player1: deque, player2: deque) -> int:
    # print()
    print(f"=== Game {game_num} ===")

    states = set()

    round = 1
    while len(player1) > 0 and len(player2) > 0:
        # Check repeated states
        p1_key = ','.join(str(c) for c in player1)
        p2_key = ','.join(str(c) for c in player2)
        key = (p1_key, p2_key)
        if key in states:
            return 1

        states.add(key)

        # print()
        # print(f'-- Round {round} --')
        # print(f"Player 1's deck: " + ', '.join(str(c) for c in player1))
        # print(f"Player 2's deck: " + ', '.join(str(c) for c in player2))

        p1_card = player1.popleft()
        p2_card = player2.popleft()
        # print(f'Player 1 plays: {p1_card}')
        # print(f'Player 2 plays: {p2_card}')

        # determine winner
        winner = 0
        if len(player1) >= p1_card and len(player2) >= p2_card:
            # print('Playing a sub-game to determine the winner...')
            winner = play_game(game_num+1, deque(list(player1)[:p1_card]), deque(list(player2)[:p2_card]))
        elif p1_card > p2_card:
            winner = 1
        elif p2_card > p1_card:
            winner = 2

        # Cleanup round
        if winner == 1:
            # print(f'Player 1 wins the round!')
            player1.append(p1_card)
            player1.append(p2_card)
        elif winner == 2:
            # print(f'Player 2 wins the round!')
            player2.append(p2_card)
            player2.append(p1_card)

        round += 1

    # winner = 1 if len(player1) else 2
    # print(f'The winner of game {game_num} is player {winner}!')
    # print()
    # print(f'...anyway, back to game {game_num-1}')
    return 1 if len(player1) else 2


if __name__ == '__main__':
    with open('input.txt') as f:
        p1deck, p2deck = parse(f.read())

    # part1(p1deck, p2deck)
    part2(p1deck, p2deck)

