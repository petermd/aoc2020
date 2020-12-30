def read(file):
    hands = []
    with open(file) as f:
        while player := f.readline().strip() != "":
            hand = []
            while (line := f.readline().strip()) != "":
                hand.append(int(line))
            hands.append(hand)
    return hands


def play(hands):
    round = 0

    while len(hands[0]) and len(hands[1]):
        round += 1
        draw = (hands[0].pop(0), hands[1].pop(0))
        if draw[0] < draw[1]:
            hands[1].extend([draw[1], draw[0]])
        else:
            hands[0].extend([draw[0], draw[1]])

    return hands[0] if len(hands[0]) else hands[1]


def partone():

    hands = read("day22.dat")

    winner = play(hands)

    total = 0
    for idx in range(1, len(winner) + 1):
        total += idx * winner[-idx]

    return total

prior_games = {}

def play_recurse(game, hands):

    loops = {}
    round = 0

    game_key = str(hands[0]) + "-" + str(hands[1])
    if game_key in prior_games:
        return prior_games[game_key]

    while len(hands[0]) and len(hands[1]):

        key = str(hands[0]) + "-" + str(hands[1])
        if key in loops:
            prior_games[game_key] = (0, hands[0] + hands[1])
            return prior_games[game_key]

        loops[key] = 1

        round += 1

        draw = (hands[0].pop(0), hands[1].pop(0))

        if draw[0] <= len(hands[0]) and draw[1] <= len(hands[1]):
            (winner, winning_hand) = play_recurse(game + 1, [hands[0][:draw[0]], hands[1][:draw[1]]])
        else:
            winner = 1 if draw[0] < draw[1] else 0

        hands[winner].append(draw[winner])
        hands[winner].append(draw[(winner + 1) % 2])

    prior_games[game_key] = (0, hands[0]) if len(hands[0]) else (1, hands[1])

    return prior_games[game_key]


def parttwo():
    hands = read("day22.dat")

    (winner, hand) = play_recurse(1, hands)

    print(winner, hand)

    total = 0
    for idx in range(1, len(hand) + 1):
        total += idx * hand[-idx]

    return total

print(partone())
print(parttwo())
