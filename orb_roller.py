# The top section is easy for Matt to edit

# RNG is fancy with this roller.
#
# There are 5 underlying seeds: one for selecting colors, and one for selecting orbs within each color category.
# Calling set_seeds() will re-roll these seeds, and giving a number to it (set_seeds(10)) will use that number as a seed for rolling the seeds
# so calling set_seeds(20) will pick the same seeds every time, but will pick different seeds than running set_seeds(21)
#
# once set_seeds() is called, roll_colors and roll_orbs will behave perfectly deterministically, even when called multiple times
# so if you call roll_colors(100) and then roll_colors(101) without calling set_seeds, you can expect the 101st roll to have
# added only one orb to the list, and have perfectly reproduced all other rolls
#
# roll_orbs works similarly for each color category, so calling roll_orbs({"blue": 40}) and
# roll_orbs({"blue": 40, "red": 40}) will generate identical blue-orb lists, and calling
# roll_orbs({"blue": 45}) will have just added 5 extra rolls to the same deterministic output

def main():
    set_seeds(123)

    # You can use randomized colors
    color_rolls = roll_colors(100)
    roll_orbs(color_rolls)

    # Or you can just specify the color to use
    roll_orbs({"blue": 30})

    # Or you can specify multiple colors to use
    roll_orbs({"blue": 30, "red": 10})


color_weights = {
    "blue": 1,
    "red": 1,
    "purple": 1,
    "green": 1
}

# Ask Christian before editing stuff below this line
# =======================================================================================================================================

import random
import csv

orb_lists = None

all_orbs = []

seed_for_color_rolls = 0
seeds_for_orb_rolls = {}

def set_seeds(seed=None):
    global seed_for_color_rolls
    if seed is None:
        seed = random.randint(0, 1000000)
    print("Using seed {}".format(seed))
    print()
    print()
    rand = random.Random()
    rand.seed(seed)
    seed_for_color_rolls = rand.getrandbits(2**20)
    for color in color_weights:
        seeds_for_orb_rolls[color] = rand.getrandbits(2**20)

def load_orb_list(fname, color):
    i = 0
    with open(fname, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        orb_lists[color] = []
        for row in reader:
            orb_id = len(all_orbs)
            orb_lists[color].append(orb_id)
            all_orbs.append(row)
            row["color"] = color
            if "weight" in row:
                row["processed_weight"] = float(row["weight"])
            else:
                row["processed_weight"] = 1
            i += 1

def load_orb_lists():
    global orb_lists
    orb_lists = {}
    load_orb_list("orb_lists/blue_orbs.csv", "blue")
    load_orb_list("orb_lists/red_orbs.csv", "red")
    load_orb_list("orb_lists/purple_orbs.csv", "purple")
    load_orb_list("orb_lists/green_orbs.csv", "green")

def select_orb_id(rand, color):
    data = []
    weights = []
    for orb_id in orb_lists[color]:
        orb_data = all_orbs[orb_id]
        data.append(orb_id)
        weights.append(orb_data["processed_weight"])
    return rand.choices(data, weights)[0]

def roll_colors(n=1):
    rand = random.Random()
    rand.seed(seed_for_color_rolls)
    colors = []
    weights = []
    for color in color_weights:
        colors.append(color)
        weights.append(color_weights[color])
    output = {}
    for _ in range(n):
        c = rand.choices(colors, weights)[0]
        if c not in output:
            output[c] = 0
        output[c] += 1
    # Pretty print output
    print("Rolling {} colors:".format(n))
    print()
    color_key_list = [n for n in output.keys()]
    color_key_list.sort()
    for c in color_key_list:
        print("{}: {}".format(c, output[c]))
    print()
    print()
    return output

def roll_orbs(color_rolls):
    if orb_lists is None:
        load_orb_lists()

    orbs_rolled_by_color = {}
    for c in color_rolls:
        orbs_rolled_by_color[c] = {}
        rand = random.Random()
        rand.seed(seeds_for_orb_rolls[c])
        for _ in range(color_rolls[c]):
            orb_id = select_orb_id(rand, c)
            if orb_id not in orbs_rolled_by_color[c]:
                orbs_rolled_by_color[c][orb_id] = 0
            orbs_rolled_by_color[c][orb_id] += 1
    color_key_list = [n for n in orbs_rolled_by_color.keys()]
    color_key_list.sort()
    for selected_color in color_key_list:
        print("{} {} orbs:".format(color_rolls[selected_color], selected_color))
        print()
        key_list = [n for n in orbs_rolled_by_color[selected_color].keys()]
        key_list.sort()
        for orb_id in key_list:
            orb_data = all_orbs[orb_id]
            print("{} ({})".format(orb_data["name"], orbs_rolled_by_color[selected_color][orb_id]))
        print()
        print()

if __name__=='__main__':
    main()