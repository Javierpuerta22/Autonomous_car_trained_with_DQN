class ServoMotor:
    def __init__(self):
        self.angle = 0
        self.direction = "LEFT"
        
    def step(self):
        if self.direction == "LEFT":
            self.angle += 10
            if self.angle >= 180:
                self.direction = "RIGHT"
        else:
            self.angle -= 10
            if self.angle <= 0:
                self.direction = "LEFT"
        
        return self.angle

    