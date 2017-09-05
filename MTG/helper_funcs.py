import traceback

def get_card_from_user_input(player, string):
    """Convert a user input (naming a card in a zone) to an actual game object

    b 2 --> 2nd(3rd) card on battlefield
    b Grizzly Bear --> Grizzly Bear on battlefield

    s 0 --> 1st card on stack (from top)

    h -1 --> last card in hand

    og 3 --> 3rd(4th) card on opponent's graveyard
    """
    if not string:
        return None

    if string[0] == 'o':  # opponent
        string = string[1:]
        player = player.game.opponent(player)

    if string[0] == 'p':
        return player

    if string[0] == 'b':
        zone = player.battlefield
    elif string[0] == 's':
        zone = player.game.stack
    elif string[0] == 'h':
        zone = player.hand
    elif string[0] == 'g':
        zone = player.graveyard
    else:
        return None

    try:
        i = int(string[2:])
        if i < len(zone):
            return zone[i]
        else:
            return None
    except ValueError:
        return zone.get_card_by_name(string[2:])


def choose_targets(source):
    if not source.target_criterias:
        return True

    print("choosing targets...\n")
    targets_chosen = []
    for criteria, prompt in zip(source.target_criterias, source.target_prompts):

        answer = source.controller.make_choice(prompt)
        card = get_card_from_user_input(source.controller, answer)
        if not card:
            return False

        try:
            if not criteria(source, card):
                return False
        except:
            traceback.print_exc()
            return False

        targets_chosen.append(card)
    return targets_chosen

def parse_targets(criterias):
    for i, v in enumerate(criterias):
        if v == 'creature':
            criterias[i] = lambda self, p: p.is_permanent and p.is_creature

        if v == 'opponent creature':
            criterias[i] = lambda self, p: p.is_creature and p.controller != self.controller

        if v == 'opponent':
            criterias[i] = lambda self, p: p.is_player and p != self

        if v == 'player':
            criterias[i] = lambda self, p: p.is_player

        if v == 'creature or player':
            criterias[i] = (lambda self, p: p.is_player
                         or (p.is_creature and p.is_permanent))

    return criterias