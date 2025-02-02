class Debuff:
    def __init__(self,duration,target):
        self.duration = duration
        self.remaining_duration = duration
        self.target = target
    def tick(self):
        self.remaining_duration -= 1
        self.effect()
        return self.remaining_duration > 0
    def name(self):
        return self.name
    def reset(self):
        self.remaining_duration = self.duration

class PoisonDebuff(Debuff):
    def __init__(self,duration,target):
        self.name = "P"
        super().__init__(duration,target)
    def effect(self):
        self.target.loosehp(0.1)
    def effectgone(self):
        pass

class SlowDebuff(Debuff):
    def __init__(self,duration,target):
        self.name = "S"
        super().__init__(duration,target)
        self.applied = False
    def effect(self):
        if self.applied == False:
            self.applied = True
            self.target.speed_modi(0.5)
    def effectgone(self):
        self.target.speed_modi(2)

