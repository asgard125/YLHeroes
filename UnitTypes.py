class Unit:
    def __init__(self, count, price):
        self.count = count
        self.price = price


# Армия нежити
class Skeleton(Unit):
    def __init__(self, count):
        super().__init__(count, 60)


class SkeletonArcher(Unit):
    def __init__(self, count):
        super().__init__(count, 80)


class Leach(Unit):
    def __init__(self, count):
        super().__init__(count, 160)


class HorsemanOfTheApocalypse(Unit):
    def __init__(self, count):
        super().__init__(count, 250)


class NecroMancer(Unit):
    def __init__(self, count):
        super().__init__(count, 300)


# Армия людей
class SpearMan(Unit):
    def __init__(self, count):
        super().__init__(count, 60)


class Arbalester(Unit):
    def __init__(self, count):
        super().__init__(count, 100)


class Cavalryman(Unit):
    def __init__(self, count):
        super().__init__(count, 250)
