import pygame

class TextComponent:
    def __init__(self, text, position, color = (255, 255, 255), font = 'default'):
        if font == 'default':
            self.font = pygame.font.SysFont('Arial', 18)
        self.text = str(text)
        self.color = color
        self.position = position
        self.component = self.font.render(str(text), True, self.color)
        
    def set_text(self, text):
        self.text = str(text)
        self.component = self.font.render(str(text), True, self.color)

    def get_x(self):
        x = self.position[0] + (self.component.get_width() // 2)
        x = min(x, self.position[0])
        return x
    
    def get_y(self):
        y = self.position[1] + (self.component.get_height() // 2)
        y = min(y, self.position[1])
        return y
    
    def get_width(self):
        return self.component.get_width()
    
    def get_height(self):
        return self.component.get_height()
    
    
class Component:
    def __init__(self, element, position, color = (0, 0, 0)):
        self.position = position
        self.element = element
        
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
        
        