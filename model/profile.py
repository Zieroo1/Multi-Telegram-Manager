class profile:
    def __init__ (self, profile):
        self.name = profile.split('_',1)[1]
        self.select = False
        self.profile = profile
        self.inst = f'tg\\{self.name}'