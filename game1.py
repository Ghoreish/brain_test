from brainmaker import Brain, mut, breed
import random
import os, time, copy


class Game:
    def __init__(self, n):
        self.player_list = []
        self.plan = []
        for i in range(n):
            self.plan.append([])
        for i in self.plan:
            for j in range(n):
                i.append(10)

    def add_player(self, x):
        self.player_list.append(x)

    def show_plan(self):
        l = copy.deepcopy(self.plan)
        for i in self.player_list:
            l[i.place[0]][i.place[1]] = "O"
        for i in l:
            row = ''
            for j in i:
                if j == 99:
                    row = row + 'X'
                elif j == 10:
                    row = row + '+'
                else:
                    row = row + '0'
            print(row)

    def add_bounties(self, n):
        bounty_list = set()
        while len(bounty_list) < n:
            x = random.randint(0, len(self.plan) - 1)
            y = random.randint(0, len(self.plan) - 1)
            self.plan[x][y] = 99
            bounty_list.add((x, y))

    def raw_plan(self):
        sample_plan = copy.deepcopy(self.plan)
        for i in self.player_list:
            sample_plan[i.place[0]][i.place[1]] = 30
        l = []
        for j in sample_plan:
            for k in j:
                l.append(k)
        return l

    def calc_points(self):
        for i in self.player_list:
            n = self.plan[i.place[0]][i.place[1]]
            if n == 99:
                i.point += 1
                self.plan[i.place[0]][i.place[1]] = 1


class Player:
    gen_id = 0

    def __init__(self, x, y, n):
        Player.gen_id += 1
        self.player_id = Player.gen_id
        self.brain = Brain(n * n)
        self.place = [x, y]
        self.plan_size = n
        self.point = 0

    def down(self):
        self.place[1] += 1
        self.place[1] %= self.plan_size

    def up(self):
        self.place[1] -= 1
        self.place[1] %= self.plan_size

    def right(self):
        self.place[0] += 1
        self.place[0] %= self.plan_size

    def left(self):
        self.place[0] -= 1
        self.place[0] %= self.plan_size

    def process(self, raw_plan):
        for i in range(len(raw_plan)):
            self.brain.pulse_to(i, raw_plan[i])
        self.brain.start_pulsing()
        x, y = self.brain.output(0, 1)
        while x >= 2 and y >= 2:
            self.brain.start_pulsing()
            x, y = self.brain.output(0, 1)
        if x == 0 and y == 0:
            self.up()
        if x == 0 and y == 1:
            self.down()
        if x == 1 and y == 0:
            self.right()
        if x == 1 and y == 1:
            self.left()


x = Game(10)
x.add_bounties(10)
for i in range(10):
    player = Player(0, 0, 10)
    player.brain.make_random_cnnection()
    x.add_player(player)

generation = 0
timer = time.time()
while True:
    timeout = 0
    for i in x.player_list:
        i.process(x.raw_plan())
    x.calc_points()
    n = 0
    for i in x.player_list:
        n += i.point
    os.system('cls')
    x.show_plan()
    print('points:', n)
    print('generation:', generation)
    time.sleep(0.1)
    if time.time() - timer > 30:
        timeout = 1
    if 99 not in x.raw_plan() or timeout == 1:
        generation += 1
        point_list = []
        for i in x.player_list:
            point_list.append(i.point)
        print(point_list)
        for i in x.player_list:
            print(i.place)
        print("done!")
        time.sleep(2)
        selected = []
        for i in x.player_list:
            if i.point > 1:
                selected.append(i)
                print(i.player_id)
        time.sleep(2)
        new_gens = []
        for i in selected:
            for j in selected:
                new_player = Player(0, 0, 10)
                new_player.brain = breed(i.brain, j.brain)
                new_gens.append(new_player)
                new_player = Player(0, 0, 10)
                new_player.brain = breed(i.brain, j.brain)
                new_player.brain = mut(new_player.brain)
                new_gens.append(new_player)
        while len(new_gens) < 10:
            new_player = Player(0, 0, 10)
            new_player.brain.make_random_cnnection()
            new_gens.append(new_player)
        while len(new_gens) > 10:
            new_gens.remove(random.choice(new_gens[9:]))
        x = Game(10)
        x.add_bounties(10)
        for i in new_gens:
            x.add_player(i)
        timer = time.time()

