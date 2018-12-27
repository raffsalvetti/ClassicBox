from vec2d import vec2d

class SystemButton:
    def __init__(self):
        self.icon = None
        self.location = vec2d(0, 0)
        self.size = vec2d(0, 0)
        self.value = None
        self.is_clicable = True
    def getBounds(self, border = 0):
        return (self.location.x + border / 2, self.location.y + border / 2, self.size.x - border, self.size.y - border)
