#!/usr/bin/env python3
"""
SLACKADEMICS - The University Group Project Survival Game
1 Human Player vs 3 AI  |  4-Player Mode  |  8 Rounds
"""

import random
import os
import sys

# ===========================================================
# UTILITIES
# ===========================================================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def go():
    input("\n  [Press Enter to continue] ")

def hr(ch="-", w=64):
    print(ch * w)

def title(text):
    w = 64
    print("=" * w)
    pad = max(0, (w - len(text)) // 2)
    print(" " * pad + text)
    print("=" * w)

def section(text):
    hr()
    print(f"  >  {text}")
    hr()

def cstr(c):
    if c == "X2":  return "[X2]"
    if c == 0:     return "[0.NoShow]"
    if c == 8:     return "[8.Desp]"
    return f"[{c}]"

def cval(c):
    return 0 if c == "X2" else (int(c) if isinstance(c, int) else 0)

def sorted_hand(hand):
    def key(c):
        return (1, 0) if c == "X2" else (0, c)
    return sorted(hand, key=key)

def pick_number(prompt, lo, hi):
    while True:
        try:
            n = int(input(prompt))
            if lo <= n <= hi:
                return n
            print(f"  Enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Please enter a number.")

# ===========================================================
# EXAM CARD DATA
# ===========================================================

EXAM_CARDS_R1_4 = [
    {"name": "PHIL 101",
     "desc": "Write a 1,000-word essay about the philosopher Haddaway's famous question: 'What is Love?'",
     "effort": 11, "cel": 2,
     "skill": "Diversity is Our Strength",
     "skill_desc": "+1 effort for each unique card value in the effort pile.",
     "blame": "highest"},
    {"name": "SOC 102",
     "desc": "Write a report on how exactly one person ends up doing all the group work.",
     "effort": 11, "cel": 2,
     "skill": "Personal Responsibility",
     "skill_desc": "The Project Leader swaps the final face-down card with one from their own hand.",
     "blame": "highest"},
    {"name": "STAT 201",
     "desc": "Prove statistically that 73% of all statistics are made up on the spot--including this one.",
     "effort": 12, "cel": 2,
     "skill": "Realign Priorities",
     "skill_desc": "Pick a player to swap the final face-down card with their top Party Pile card.",
     "blame": "accuse"},
    {"name": "BIO 215",
     "desc": "Memorize every organ in the human body, then forget them immediately after the exam.",
     "effort": 12, "cel": 2,
     "skill": "Pull an All Nighter",
     "skill_desc": "Pick 2 players: each plays an extra effort card from their hand (no party card this round).",
     "blame": "accuse"},
    {"name": "MKTG 250",
     "desc": "Create a campaign convincing people they need something they've lived without for 20 years.",
     "effort": 13, "cel": 2,
     "skill": "Round of Coffee",
     "skill_desc": "All effort pile cards with value 1 or 2 are doubled.",
     "blame": "highest"},
    {"name": "CSCI 220",
     "desc": "Write code that works perfectly... until the professor runs it.",
     "effort": 13, "cel": 2,
     "skill": "Extend the Deadline",
     "skill_desc": "Each player picks up a card from the effort pile, then replays an effort card face-up.",
     "blame": "accuse"},
    {"name": "HIST 305",
     "desc": "Explain a historical event through badly labeled maps and vague dates like 'the late 1800s.'",
     "effort": 14, "cel": 2,
     "skill": "Plagiarize",
     "skill_desc": "Any X2 cards in the effort pile become X3 instead.",
     "blame": "highest"},
    {"name": "PSYC 290",
     "desc": "Design an experiment proving that procrastination is a legitimate time management strategy.",
     "effort": 14, "cel": 2,
     "skill": "Curve the Grade",
     "skill_desc": "Subtract 6 from effort required. Add 6 to the next exam's effort.",
     "blame": "accuse"},
]

EXAM_CARDS_R5_8 = [
    {"name": "ECON 302",
     "desc": "Explain why textbooks cost $300 using supply and demand curves.",
     "effort": 15, "cel": 3,
     "skill": "Diversity is Our Strength",
     "skill_desc": "+1 effort for each unique card value in the effort pile.",
     "blame": "highest"},
    {"name": "ENGR 401",
     "desc": "Build a project where the math works but the physical object absolutely does not.",
     "effort": 15, "cel": 3,
     "skill": "Personal Responsibility",
     "skill_desc": "The Project Leader swaps the final face-down card with one from their own hand.",
     "blame": "highest"},
    {"name": "ENGL 315",
     "desc": "Write 5,000 words analyzing why the curtains were blue (the author just liked blue).",
     "effort": 16, "cel": 3,
     "skill": "Realign Priorities",
     "skill_desc": "Pick a player to swap the final face-down card with their top Party Pile card.",
     "blame": "accuse"},
    {"name": "CHEM 340",
     "desc": "Mix clear liquids together and explain why the result is somehow purple and mildly alarming.",
     "effort": 16, "cel": 3,
     "skill": "Pull an All Nighter",
     "skill_desc": "Pick 2 players: each plays an extra effort card from their hand (no party card this round).",
     "blame": "accuse"},
    {"name": "BUSN 420",
     "desc": "Analyze why Netflix keeps canceling good shows after one season. Cite your sources.",
     "effort": 17, "cel": 3,
     "skill": "Round of Coffee",
     "skill_desc": "All effort pile cards with value 1 or 2 are doubled.",
     "blame": "highest"},
    {"name": "PHYS 350",
     "desc": "Prove thermodynamics is real by explaining why your dorm room entropy only increases.",
     "effort": 17, "cel": 3,
     "skill": "Extend the Deadline",
     "skill_desc": "Each player picks up a card from the effort pile, then replays an effort card face-up.",
     "blame": "accuse"},
    {"name": "ART 275",
     "desc": "Create a piece of art and write a 3-page explanation of what it 'really' means.",
     "effort": 18, "cel": 3,
     "skill": "Plagiarize",
     "skill_desc": "Any X2 cards in the effort pile become X3 instead.",
     "blame": "accuse"},
    {"name": "MUSC 380",
     "desc": "Compose a symphony or just sample Pachelbel's Canon like everybody else does.",
     "effort": 21, "cel": 3,
     "skill": "Leave the Group",
     "skill_desc": "Discard the final face-down card (unrevealed). Reduce effort by 3. Immune from blame.",
     "blame": "highest"},
]

ALL_SKILLS = [
    "Diversity is Our Strength", "Personal Responsibility", "Realign Priorities",
    "Pull an All Nighter", "Round of Coffee", "Extend the Deadline",
    "Plagiarize", "Curve the Grade", "Leave the Group",
]

# ===========================================================
# PLAYER
# ===========================================================

class Player:
    def __init__(self, name, is_human=False, slack=0.70):
        self.name = name
        self.is_human = is_human
        self.slack = slack       # AI: fraction of fair share to contribute (lower = more slacking)
        self.hand = []
        self.party_pile = []
        self.fail_markers = 0
        self.halftime_pts = 0
        self.cel_pts = 0
        self.eliminated = False
        self.immune_blame = False

    def build_hand(self, no_show=False, desperation=False):
        self.hand = [1, 2, 3, 4, 5, 6, 7, "X2"]
        if no_show:
            self.hand[self.hand.index(1)] = 0    # No Show replaces 1
        if desperation:
            self.hand[self.hand.index(7)] = 8    # Desperation replaces 7

    def party_total(self):
        return sum(c for c in self.party_pile if isinstance(c, int))

    def score(self):
        return self.halftime_pts + self.party_total() + self.cel_pts

    def top_party_val(self):
        for c in reversed(self.party_pile):
            if isinstance(c, int):
                return c
        return 0

    def discard_top_party(self):
        for i in range(len(self.party_pile) - 1, -1, -1):
            if isinstance(self.party_pile[i], int):
                return self.party_pile.pop(i)
        return None

    def has_non_x2(self):
        return any(c != "X2" for c in self.hand)

    def ai_pick_effort(self, effort_req, num_active):
        numeric = sorted([c for c in self.hand if isinstance(c, int)])
        has_x2 = "X2" in self.hand

        if not numeric and not has_x2:
            return None
        if not numeric:
            return "X2"

        fair = effort_req / max(num_active, 1)
        roll = random.randint(0, 3)

        # Strategy 0 (25%): Play X2 — reroll 1-3 if X2 already used
        if roll == 0:
            if has_x2:
                return "X2"
            roll = random.randint(1, 3)

        # Strategy 1 (25%): Asshole — play lowest card to effort pile
        if roll == 1:
            return min(numeric)

        # Strategy 2 (25%): Fair share — play card closest to effort_req / num_active
        if roll == 2:
            return min(numeric, key=lambda c: abs(c - fair))

        # Strategy 3 (25%): Generous — random card at or above fair share
        above = [c for c in numeric if c >= fair]
        return random.choice(above) if above else max(numeric)

    def ai_pick_party(self, exclude):
        choices = [c for c in self.hand if c != "X2" and c != exclude]
        if not choices:
            choices = [c for c in self.hand if c != "X2"]
        if not choices:
            return None
        return max(choices)

    def __str__(self):
        return self.name


# ===========================================================
# DISPLAY
# ===========================================================

def show_status(players, round_num, leader, exam=None):
    clear()
    title(f"SLACKADEMICS  .  Round {round_num} / 8")
    if exam:
        print(f"\n  Exam: {exam['name']}  |  Effort needed: {exam['effort']}  |  +{exam['cel']} Celebration Points")
    print()
    hr("-")
    print(f"  {'':2}{'PLAYER':<14} {'PARTY':>6} {'CEL':>5} {'HALF':>5} {'TOTAL':>6}  FAILS  HAND")
    hr("-")
    for p in players:
        marker = " *" if p == leader else "  "
        fails_str = "#" * p.fail_markers + "." * (4 - p.fail_markers)
        expelled = "  [EXPELLED]" if p.eliminated else ""
        h_str = " ".join(cstr(c) for c in sorted_hand(p.hand)) if not p.eliminated else "(no cards)"
        print(f"{marker}{p.name:<14} {p.party_total():>6} {p.cel_pts:>5} {p.halftime_pts:>5} {p.score():>6}  {fails_str}{expelled}")
        if not p.eliminated:
            print(f"    Hand: {h_str}")
    hr("-")
    print(f"  * = Project Leader  |  # = Fail Marker (4 = Expelled)")
    print()

def show_party_piles(players):
    print("\n  PARTY PILES:")
    for p in [x for x in players if not x.eliminated]:
        pile = " ".join(cstr(c) for c in p.party_pile) if p.party_pile else "(empty)"
        print(f"    {p.name}: {pile}  [{p.party_total()} pts]")
    print()


# ===========================================================
# EFFORT CALCULATION
# ===========================================================

def compute_effort(pile, x3_x2=False):
    """
    Compute total effort from a pile of cards.
    X2 doubles the highest available card; if x3_x2=True (Plagiarize), X2 triples instead.
    """
    numerics = sorted([c for c in pile if isinstance(c, int)], reverse=True)
    x2_count = pile.count("X2")
    total = sum(numerics)
    multiplier = 2 if not x3_x2 else 3
    for i in range(min(x2_count, len(numerics))):
        total += numerics[i] * (multiplier - 1)  # e.g. double = +1x, triple = +2x
    return total


# ===========================================================
# PLAY CARDS PHASE
# ===========================================================

def human_pick_from(hand, label, can_x2=True):
    """Ask human to pick a card. can_x2=False excludes X2."""
    valid = sorted_hand([c for c in hand if (can_x2 or c != "X2")])
    if not valid:
        return None
    print(f"  Choose a card for {label}:")
    for i, c in enumerate(valid):
        note = "  (can ONLY go to effort pile)" if c == "X2" else ""
        print(f"    {i+1}. {cstr(c)}{note}")
    ch = pick_number("  > ", 1, len(valid))
    return valid[ch - 1]

def play_cards_phase(active, leader, exam):
    """
    Each active player secretly picks 1 effort card + 1 party card.
    Returns effort_pile (shuffled), after placing party cards face-up.
    """
    effort_assignments = {}
    party_assignments = {}
    fair = exam["effort"] // len(active)

    print(f"\n  Each player secretly chooses 1 card for the effort pile and 1 for their Party Pile.")
    print(f"  Effort needed: {exam['effort']}  |  Fair share per player: ~{fair}\n")

    for p in active:
        if p.is_human:
            print(f"  YOUR TURN, {p.name}!")
            print(f"  Your hand: {' '.join(cstr(c) for c in sorted_hand(p.hand))}")
            print(f"  Party Pile: {' '.join(cstr(c) for c in p.party_pile) or '(empty)'}")
            print()
            # Pick effort card (any card, including X2)
            ec = human_pick_from(p.hand, "the EFFORT PILE (helps the group)", can_x2=True)
            temp = list(p.hand)
            temp.remove(ec)
            # Pick party card (not X2)
            non_x2 = [c for c in temp if c != "X2"]
            if non_x2:
                pc = human_pick_from(temp, "your PARTY PILE (your points!)", can_x2=False)
            else:
                print("  No valid party card (only X2 left -- it can't go to Party Pile).")
                pc = None
            effort_assignments[p] = ec
            party_assignments[p] = pc
            print()
        else:
            ec = p.ai_pick_effort(exam["effort"], len(active))
            if ec is None:
                ec = p.hand[0]
            pc = p.ai_pick_party(ec)
            effort_assignments[p] = ec
            party_assignments[p] = pc
            print(f"  {p.name} has played their cards secretly.")

    # Place party cards face-up
    print("\n  Party cards played face-up:")
    for p in active:
        pc = party_assignments[p]
        if pc is not None and pc in p.hand:
            p.hand.remove(pc)
            p.party_pile.append(pc)
            print(f"    {p.name} -> Party Pile: {cstr(pc)}")
        else:
            print(f"    {p.name} -> no party card this round")

    # Collect effort cards
    effort_pile = []
    for p in active:
        ec = effort_assignments[p]
        if ec is not None and ec in p.hand:
            p.hand.remove(ec)
            effort_pile.append(ec)

    random.shuffle(effort_pile)
    print(f"\n  Effort pile collected and shuffled ({len(effort_pile)} cards face-down).")
    return effort_pile


# ===========================================================
# REVEAL PHASE
# ===========================================================

def reveal_phase(effort_pile, effort_req):
    """
    Reveal all but the last card one at a time.
    Returns (revealed, last_card, revealed_total, remaining).
    """
    section("THE REVEAL")
    pile = list(effort_pile)
    revealed = []

    print(f"  Effort needed: {effort_req}")
    print(f"  Revealing cards one by one...\n")

    while len(pile) > 1:
        card = pile.pop(0)
        revealed.append(card)
        print(f"  > {cstr(card)}", end="")
        if card == "X2":
            print("  (doubles the highest card!)", end="")
        print()
        inp = input("    [Enter to continue, or type 'skip'] ").strip().lower()
        if inp == "skip":
            while len(pile) > 1:
                card = pile.pop(0)
                revealed.append(card)
                print(f"  > {cstr(card)}")
            break

    last_card = pile[0]
    revealed_total = compute_effort(revealed)
    remaining = effort_req - revealed_total

    print(f"\n  Cards revealed: {' '.join(cstr(c) for c in revealed)}")
    print(f"  Effort so far:  {revealed_total} / {effort_req}")
    print(f"  Still needed:   {remaining}")
    print(f"\n  One card remains face-down:  [?]")

    return revealed, last_card, revealed_total, remaining


# ===========================================================
# LEADERSHIP SKILLS
# ===========================================================

def apply_skill(skill, exam, effort_pile, last_card, effort_req,
                players, leader, active, game_state):
    """
    Apply the chosen leadership skill.
    Returns (effort_pile, effort_req, last_card).
    """
    print(f"\n  Applying: {skill}")
    print(f"  -------------------------------------")

    if skill == "Diversity is Our Strength":
        unique = set()
        for c in effort_pile:
            if isinstance(c, int):
                unique.add(c)
            else:
                unique.add("X2")
        bonus = len(unique)
        print(f"  {bonus} unique card values -> effort required reduced by {bonus}!")
        effort_req -= bonus

    elif skill == "Personal Responsibility":
        if not leader.hand:
            print(f"  {leader.name} has no cards to swap. Skill fizzles.")
        else:
            if leader.is_human:
                print(f"  Your hand: {' '.join(cstr(c) for c in sorted_hand(leader.hand))}")
                print(f"  Swap the face-down card {cstr(last_card)} with one from your hand.")
                swap = human_pick_from(leader.hand, "swap into effort pile", can_x2=False)
            else:
                numeric = sorted([c for c in leader.hand if isinstance(c, int)], reverse=True)
                swap = numeric[0] if numeric else None

            if swap and swap in leader.hand:
                leader.hand.remove(swap)
                leader.hand.append(last_card)
                # Replace last_card in effort_pile
                idx = next((i for i in range(len(effort_pile)-1, -1, -1)
                            if effort_pile[i] == last_card), -1)
                if idx >= 0:
                    effort_pile[idx] = swap
                else:
                    effort_pile.append(swap)
                last_card = swap
                print(f"  {leader.name} swaps in {cstr(swap)} -- face-down card replaced!")
            else:
                print(f"  No valid swap card found.")

    elif skill == "Realign Priorities":
        targets = [p for p in active if p != leader and p.party_pile]
        if not targets:
            print("  No players have party cards. Skill fizzles.")
        else:
            if leader.is_human:
                print("  Pick a player to swap the face-down card with their top Party card:")
                for i, t in enumerate(targets):
                    print(f"    {i+1}. {t.name}  (top party card: {cstr(t.party_pile[-1])})")
                ch = pick_number("  > ", 1, len(targets)) - 1
                target = targets[ch]
            else:
                target = max(targets, key=lambda p: p.top_party_val())

            top = target.party_pile.pop()
            target.party_pile.append(last_card)
            idx = next((i for i in range(len(effort_pile)-1, -1, -1)
                        if effort_pile[i] == last_card), -1)
            if idx >= 0:
                effort_pile[idx] = top
            else:
                effort_pile.append(top)
            last_card = top
            print(f"  {target.name}'s top party card {cstr(top)} -> effort pile!")
            print(f"  Face-down card {cstr(last_card)} -> {target.name}'s party pile!")

    elif skill == "Pull an All Nighter":
        others = [p for p in active if p != leader and
                  any(isinstance(c, int) for c in p.hand)]
        if len(others) < 1:
            print("  No valid targets. Skill fizzles.")
        else:
            n_targets = min(2, len(others))
            if leader.is_human:
                print(f"  Pick {n_targets} player(s) to pull an all-nighter:")
                for i, p in enumerate(others):
                    print(f"    {i+1}. {p.name}")
                chosen = []
                while len(chosen) < n_targets:
                    ch = pick_number(f"  Player {len(chosen)+1}: ", 1, len(others)) - 1
                    if others[ch] not in chosen:
                        chosen.append(others[ch])
                    else:
                        print("  Already chosen.")
            else:
                chosen = random.sample(others, n_targets)

            for t in chosen:
                extra = t.ai_pick_effort(effort_req, len(active)) if not t.is_human \
                    else human_pick_from(t.hand, f"{t.name}'s extra effort card", can_x2=False)
                if extra and extra in t.hand:
                    t.hand.remove(extra)
                    effort_pile.append(extra)
                    print(f"  {t.name} plays extra {cstr(extra)} to effort pile!")

            random.shuffle(effort_pile)
            print("  Effort pile reshuffled!")
            # Re-find last_card position (last in pile now)
            last_card = effort_pile[-1]

    elif skill == "Round of Coffee":
        ones_twos = [c for c in effort_pile if isinstance(c, int) and c in (1, 2)]
        bonus = sum(ones_twos)
        print(f"  All 1s and 2s doubled -> effort required reduced by {bonus}!")
        effort_req -= bonus

    elif skill == "Extend the Deadline":
        print("  Each player picks up a card from the effort pile, then replays!")
        old_pile = list(effort_pile)
        for p in active:
            if not old_pile:
                break
            if p.is_human:
                print(f"\n  Effort pile: {' '.join(cstr(c) for c in old_pile)}")
                print(f"  Your hand: {' '.join(cstr(c) for c in sorted_hand(p.hand))}")
                print("  Pick up a card from the effort pile:")
                for i, c in enumerate(old_pile):
                    print(f"    {i+1}. {cstr(c)}")
                ch = pick_number("  > ", 1, len(old_pile)) - 1
                picked = old_pile.pop(ch)
            else:
                picked = old_pile.pop(random.randrange(len(old_pile)))
            p.hand.append(picked)
            print(f"  {p.name} picks up {cstr(picked)}")

        effort_pile.clear()
        print()
        for p in active:
            if not p.hand:
                continue
            if p.is_human:
                print(f"  Your hand: {' '.join(cstr(c) for c in sorted_hand(p.hand))}")
                replay = human_pick_from(p.hand, "replay to effort pile", can_x2=True)
            else:
                replay = p.ai_pick_effort(effort_req, len(active))
                if replay not in p.hand:
                    numeric = [c for c in p.hand if isinstance(c, int)]
                    replay = numeric[0] if numeric else (p.hand[0] if p.hand else None)
            if replay and replay in p.hand:
                p.hand.remove(replay)
                effort_pile.append(replay)
                print(f"  {p.name} replays {cstr(replay)}")

        random.shuffle(effort_pile)
        last_card = effort_pile[-1] if effort_pile else last_card

    elif skill == "Plagiarize":
        x2_count = effort_pile.count("X2")
        if x2_count == 0:
            print("  No X2 cards in pile. Skill fizzles!")
        else:
            numerics = sorted([c for c in effort_pile if isinstance(c, int)], reverse=True)
            bonus = sum(numerics[i] for i in range(min(x2_count, len(numerics))))
            print(f"  {x2_count} X2 card(s) -> X3! +{bonus} extra effort!")
            effort_req -= bonus

    elif skill == "Curve the Grade":
        print(f"  Effort reduced by 6 (from {effort_req} to {effort_req - 6}).")
        effort_req -= 6
        game_state["next_exam_bonus"] += 6
        print(f"  Next exam will be 6 harder!")

    elif skill == "Leave the Group":
        print(f"  Discarding the final face-down card {cstr(last_card)} without revealing!")
        if last_card in effort_pile:
            effort_pile.remove(last_card)
        effort_req -= 3
        leader.immune_blame = True
        print(f"  Effort reduced by 3 (now {effort_req}).")
        print(f"  {leader.name} is immune from blame this round.")
        # Update last_card (pile might now be empty or have new last)
        last_card = effort_pile[-1] if effort_pile else None

    print(f"  -------------------------------------")
    return effort_pile, effort_req, last_card


# ===========================================================
# DAY OF THE DEADLINE
# ===========================================================

def day_of_deadline(players, leader, revealed, last_card,
                    effort_req, exam, game_state):
    """
    Project Leader chooses: Let it Ride or Use a Leadership Skill.
    Returns (final_pile, final_req, used_skill, final_total).
    """
    section("*  DAY OF THE DEADLINE  *")
    active = [p for p in players if not p.eliminated]
    skills = game_state["skills_available"]
    used_skill = False

    print(f"  Project Leader: {leader.name}")
    print(f"  Cards revealed: {' '.join(cstr(c) for c in revealed)}")
    print(f"  Effort so far:  {compute_effort(revealed)} / {effort_req}")
    remaining = effort_req - compute_effort(revealed)
    print(f"  One card remains face-down: [?]  (need {remaining} more)")
    print()
    if skills:
        print(f"  Leadership skills available: {', '.join(skills)}")
    else:
        print(f"  No leadership skills available yet.")
    print(f"  (Earn skills by passing rounds with 'Let it Ride')")
    print()

    effort_pile = revealed + [last_card]

    if leader.is_human:
        print("  What do you do?")
        print("    1. Let it Ride (flip the last card!)")
        if skills:
            print("    2. Use a Leadership Skill")
        choice = pick_number("  > ", 1, 2 if skills else 1)
        used_skill = (choice == 2)
    else:
        # AI logic: use skill if deficit is large
        deficit = effort_req - compute_effort(effort_pile[:-1])  # worst case: last card = 0
        if deficit > 5 and skills:
            used_skill = True
        # Let it ride otherwise
        if used_skill:
            print(f"  {leader.name} decides to USE A LEADERSHIP SKILL!")
        else:
            print(f"  {leader.name} decides to LET IT RIDE!")

    if used_skill:
        if leader.is_human:
            print(f"\n  Choose a skill:")
            for i, s in enumerate(skills):
                print(f"    {i+1}. {s}")
            ch = pick_number("  > ", 1, len(skills)) - 1
            skill_name = skills[ch]
        else:
            skill_name = skills[0]

        print(f"\n  Using: [{skill_name}]")
        skills.remove(skill_name)

        effort_pile, effort_req, last_card = apply_skill(
            skill_name, exam, effort_pile, last_card, effort_req,
            players, leader, active, game_state
        )

    # Reveal the final card (if it's still in the pile and not discarded)
    print(f"\n  Revealing final effort pile...")
    if effort_pile:
        print(f"  Final pile: {' '.join(cstr(c) for c in effort_pile)}")

    final_total = compute_effort(effort_pile)
    print(f"\n  FINAL EFFORT TOTAL: {final_total} / {effort_req}")

    return effort_pile, effort_req, used_skill, final_total


# ===========================================================
# FAIL PROCEDURE
# ===========================================================

def handle_blame(players, leader, active):
    """Run the blame vote for a major fail."""
    blameable = [p for p in active if p != leader and not p.immune_blame and not p.eliminated]
    if not blameable:
        print(f"\n  No one can be blamed (everyone is immune or it's just the leader).")
        for p in players:
            p.immune_blame = False
        return

    print(f"\n  [BLAME]  BLAME TIME! {leader.name} must accuse someone.")

    if leader.is_human:
        print("  Who do you accuse?")
        for i, p in enumerate(blameable):
            print(f"    {i+1}. {p.name}")
        ch = pick_number("  > ", 1, len(blameable)) - 1
        accused = blameable[ch]
    else:
        accused = random.choice(blameable)
        print(f"  {leader.name} accuses {accused.name}!")

    # Vote: everyone except leader and accused
    voters = [p for p in active if p != leader and p != accused and not p.eliminated]
    yes, no = 0, 0
    print(f"\n  Vote: Is {accused.name} responsible? (majority = guilty)")
    for v in voters:
        if v.is_human:
            ans = input(f"  {v.name}, vote (y/n): ").strip().lower()
            vote = ans in ('y', 'yes')
        else:
            vote = random.random() < 0.55
        if vote:
            yes += 1
            print(f"    {v.name}: [YES] GUILTY")
        else:
            no += 1
            print(f"    {v.name}: [NO] NOT GUILTY")

    needed = max(1, len(voters) * 0.5)
    if len(voters) == 0 or yes >= needed:
        print(f"\n  Verdict: {yes}-{no} GUILTY -> {accused.name} gets a personal fail marker!")
        accused.fail_markers += 1
    else:
        print(f"\n  Verdict: {yes}-{no} NOT GUILTY")
        print(f"  {accused.name} may redirect blame to {leader.name}!")

        if accused.is_human:
            ans = input(f"  Redirect blame to {leader.name}? (y/n): ").strip().lower()
            redirect = ans in ('y', 'yes')
        else:
            redirect = random.random() < 0.6

        if redirect:
            print(f"\n  {accused.name} points the finger at {leader.name}!")
            voters2 = [p for p in active if p != leader and not p.eliminated]
            yes2 = 0
            for v in voters2:
                if v.is_human:
                    ans = input(f"  {v.name}, vote guilty on {leader.name}? (y/n): ").strip().lower()
                    vote = ans in ('y', 'yes')
                else:
                    vote = random.random() < 0.5
                if vote:
                    yes2 += 1
            if yes2 >= max(1, len(voters2) * 0.5):
                print(f"  {leader.name} found GUILTY! Personal fail marker added!")
                leader.fail_markers += 1
            else:
                print(f"  {leader.name} also NOT GUILTY. No extra blame.")
        else:
            print(f"  Blame dropped. No extra fail markers.")

    for p in players:
        p.immune_blame = False


def fail_procedure(players, leader, is_major, exam, game_state, used_skill):
    """Handle fail consequences. Returns list of newly eliminated players."""
    if used_skill:
        is_major = True  # always major if skill was used and still failed

    active = [p for p in players if not p.eliminated]

    print(f"\n  {'*** MAJOR' if is_major else '!!  MINOR'} FAIL!")
    print(f"  Everyone gets 1 fail marker.")
    for p in active:
        p.fail_markers += 1

    if is_major:
        print(f"\n  MAJOR FAIL: Everyone discards their top Party Pile card!")
        for p in active:
            d = p.discard_top_party()
            if d is not None:
                print(f"    {p.name} discards {cstr(d)}")
            else:
                print(f"    {p.name}: nothing to discard")
        handle_blame(players, leader, active)
    else:
        # Minor fail: only highest top-card player discards
        top_vals = {p: p.top_party_val() for p in active}
        max_v = max(top_vals.values()) if top_vals else 0
        if max_v > 0:
            to_lose = [p for p, v in top_vals.items() if v == max_v]
            print(f"\n  MINOR FAIL: Player(s) with highest top Party card ({max_v}) discard it:")
            for p in to_lose:
                d = p.discard_top_party()
                print(f"    {p.name} discards {cstr(d)}")
        else:
            print(f"\n  MINOR FAIL: No party cards to discard.")

    # Check for new eliminations
    newly_expelled = []
    for p in active:
        if p.fail_markers >= 4 and not p.eliminated:
            p.eliminated = True
            newly_expelled.append(p)
            print(f"\n  >>  {p.name} has been EXPELLED! (4 fail markers)")

    return newly_expelled


# ===========================================================
# HALFTIME
# ===========================================================

def halftime(players):
    clear()
    title("*  HALFTIME  *")
    active = [p for p in players if not p.eliminated]

    print("\n  Rounds 1-4 complete! Recording halftime scores...\n")

    ranked = sorted(active, key=lambda p: p.party_total() + p.cel_pts, reverse=True)

    print("  HALFTIME RANKINGS:")
    hr("-")
    for rank, p in enumerate(ranked, 1):
        ht = p.party_total() + p.cel_pts
        print(f"  {rank}. {p.name:<14}  Party: {p.party_total():>3}  Cel: {p.cel_pts:>3}  = {ht:>3} pts")
    hr("-")

    for p in active:
        p.halftime_pts = p.party_total() + p.cel_pts

    print("\n  Resetting Party Piles and rebuilding hands...")
    n = len(ranked)
    for rank, p in enumerate(ranked, 1):
        no_show = rank <= 2
        desperation = rank >= n - 1  # bottom 2
        p.party_pile = []
        p.build_hand(no_show=no_show, desperation=desperation)
        mods = []
        if no_show:      mods.append("No Show (1->0)")
        if desperation:  mods.append("Desperation (7->8)")
        tag = f"  [{', '.join(mods)}]" if mods else ""
        print(f"  {p.name} (rank {rank}): new hand {' '.join(cstr(c) for c in sorted_hand(p.hand))}{tag}")

    print()
    go()


# ===========================================================
# END GAME
# ===========================================================

def end_game(players):
    clear()
    title("*  GAME OVER -- FINAL SCORES  *")
    print()
    hr("-")
    print(f"  {'PLAYER':<14} {'HALF':>6} {'PARTY':>7} {'CEL':>5}  {'TOTAL':>7}  STATUS")
    hr("-")
    scores = [(p, p.halftime_pts + p.party_total() + p.cel_pts) for p in players]
    scores.sort(key=lambda x: x[1], reverse=True)
    for p, total in scores:
        status = "[EXPELLED]" if p.eliminated else ""
        print(f"  {p.name:<14} {p.halftime_pts:>6} {p.party_total():>7} {p.cel_pts:>5}  {total:>7}  {status}")
    hr("-")
    winner, best = scores[0]
    print(f"\n  >>  WINNER: {winner.name}  with  {best} points!")
    if winner.is_human:
        print("\n  You partied hard AND survived university. Absolute legend.")
    else:
        print(f"\n  {winner.name} out-slacked the competition. Better luck next semester!")
    print()


# ===========================================================
# MAIN GAME LOOP
# ===========================================================

def main():
    clear()
    title("SLACKADEMICS")
    print("""
  The University Group Project Survival Game
  1 Human Player  vs  3 AI Opponents  |  8 Rounds

  Goal: Accumulate the most party points without
  collecting 4 fail markers (= expelled!).

  Each round, secretly contribute one effort card to the
  group project and place one card face-up in your Party
  Pile. Pass the project to score -- but slack enough to
  keep those high cards for yourself!
""")
    human_name = input("  Enter your name: ").strip() or "You"

    # Create players
    players = [
        Player(human_name, is_human=True),
        Player("Alex",   is_human=False, slack=0.88),  # light slacker
        Player("Sam",    is_human=False, slack=0.80),  # moderate slacker
        Player("Jordan", is_human=False, slack=0.72),  # heavy freeloader
    ]
    for p in players:
        p.build_hand()

    # Shuffle decks
    deck14 = list(EXAM_CARDS_R1_4)
    deck58 = list(EXAM_CARDS_R5_8)
    random.shuffle(deck14)
    random.shuffle(deck58)

    # Skill deck (shuffled)
    skill_deck = list(ALL_SKILLS)
    random.shuffle(skill_deck)

    # Game state
    game_state = {
        "skills_available": [],
        "next_exam_bonus": 0,
    }

    # Draw 1 starting skill
    if skill_deck:
        starting_skill = skill_deck.pop(0)
        game_state["skills_available"].append(starting_skill)
        print(f"\n  Starting Leadership Skill: [{starting_skill}]")

    # Random first leader
    leader_idx = random.randint(0, len(players) - 1)
    print(f"  First Project Leader: {players[leader_idx].name}")
    go()

    # -- MAIN LOOP ------------------------------------------
    for round_num in range(1, 9):
        active = [p for p in players if not p.eliminated]

        # End early if <= 1 active
        if len(active) <= 1:
            break

        # Find leader (skip eliminated)
        while players[leader_idx].eliminated:
            leader_idx = (leader_idx + 1) % len(players)
        leader = players[leader_idx]

        # Get exam card
        exam = dict(deck14[round_num - 1] if round_num <= 4 else deck58[round_num - 5])

        # Apply next-exam difficulty bonus (from Curve the Grade)
        if game_state["next_exam_bonus"]:
            exam["effort"] += game_state["next_exam_bonus"]
            print(f"  (Effort boosted by +{game_state['next_exam_bonus']} from previous Curve the Grade!)")
            game_state["next_exam_bonus"] = 0

        # -- SHOW STATUS & EXAM CARD ------------------------
        show_status(players, round_num, leader, exam)
        section(f"ROUND {round_num}  .  {exam['name']}")
        print(f"\n  \"{exam['desc']}\"")
        print(f"\n  Effort Required: {exam['effort']}   Celebration: +{exam['cel']} pts")
        print(f"  Leadership Skill on this card: [{exam['skill']}]")
        print(f"  ({exam['skill_desc']})")
        print(f"\n  Project Leader: {leader.name}")

        # Motivational speech
        print()
        hr(".")
        print("  MOTIVATIONAL SPEECH:")
        if leader.is_human:
            print("  You're the Project Leader! Say something inspiring (or press Enter):")
            speech = input("  > ").strip()
            if not speech:
                speech = "\"Come on everyone, just... try? A little bit?\""
            print(f"  You say: {speech}")
        else:
            speeches = [
                f'"{leader.name}: Look, we just need to pass. Don\'t overthink it."',
                f'"{leader.name}: Everyone just play a 3. I\'m definitely going to. Probably."',
                f'"{leader.name}: If we all pitch in a tiny bit, we\'ll totally nail this!"',
                f'"{leader.name}: I have full confidence in this team. By which I mean myself."',
                f'"{leader.name}: This one\'s easy. Trust the process. My process."',
            ]
            print(f"  {random.choice(speeches)}")
        hr(".")
        go()

        # -- PLAY CARDS -------------------------------------
        show_status(players, round_num, leader, exam)
        effort_pile = play_cards_phase(active, leader, exam)
        show_party_piles(active)
        go()

        # -- REVEAL -----------------------------------------
        revealed, last_card, rev_total, remaining = reveal_phase(effort_pile, exam["effort"])
        go()

        # -- DAY OF THE DEADLINE ----------------------------
        final_pile, final_req, used_skill, final_total = day_of_deadline(
            players, leader, revealed, last_card,
            exam["effort"], exam, game_state
        )
        go()

        # -- PASS / FAIL ------------------------------------
        section("RESULT")
        if final_total >= final_req:
            print(f"\n  [PASS]  PROJECT PASSED!  ({final_total} / {final_req})")

            if not used_skill:
                # Leader earns celebration points + draws a skill
                print(f"\n  {leader.name} earns {exam['cel']} Celebration Points!")
                leader.cel_pts += exam["cel"]

                # Give 2 bonus celebration points
                others = [p for p in active if p != leader]
                if others:
                    if leader.is_human:
                        print(f"\n  Award 2 bonus Celebration Points to someone who helped:")
                        for i, p in enumerate(others):
                            print(f"    {i+1}. {p.name}")
                        print(f"    0. Skip")
                        ch = pick_number("  > ", 0, len(others))
                        if ch > 0:
                            others[ch - 1].cel_pts += 2
                            print(f"  {others[ch - 1].name} gets 2 bonus Celebration Points!")
                    else:
                        rec = random.choice(others)
                        rec.cel_pts += 2
                        print(f"  {leader.name} awards 2 bonus Celebration Points to {rec.name}!")

                # Earn a leadership skill card
                if skill_deck:
                    new_skill = skill_deck.pop(0)
                    game_state["skills_available"].append(new_skill)
                    print(f"\n  Leadership Skill earned: [{new_skill}]")
                    print(f"  (Now available for future rounds!)")
            else:
                print(f"  (No celebration points -- a skill was used.)")
        else:
            shortfall = final_req - final_total
            is_major = shortfall >= len(active)
            print(f"\n  [FAIL]  PROJECT FAILED!  ({final_total} / {final_req}  |  short by {shortfall})")
            fail_procedure(players, leader, is_major, exam, game_state, used_skill)

        go()
        show_party_piles(active)
        show_status(players, round_num, leader)

        # -- HALFTIME ---------------------------------------
        if round_num == 4:
            go()
            halftime(players)

        # -- ROTATE LEADER ----------------------------------
        leader_idx = (leader_idx + 1) % len(players)

        # Check if game ends early
        active_check = [p for p in players if not p.eliminated]
        if len(active_check) <= 1:
            break

        go()

    # -- END GAME -------------------------------------------
    end_game(players)


if __name__ == "__main__":
    main()
