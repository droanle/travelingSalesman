import pygame

class EventHandler:
    def __init__(self, origin):
        self.event = None
        self.events = []
        self.origin = origin
        
    def get_events(self):
        event = self.event
        self.event = None
        return event
    
    def proccess_events(self):
        if self.event is not None: 
            self.event = None
            return True
        return False
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event = 'exit'
                pygame.display.quit()
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.event = 1
                self.mouse_button_down(event)
                
            if event.type == pygame.KEYDOWN:
                self.key_down(event)
            
    
    def mouse_button_down(self, event):
        if event.button == 1:
            print(event.pos)
        elif event.button == 2:
            pass
        elif event.button == 3:
            pass
        else:
            print('no event')
        pass
                
    def key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.display.quit()
            pygame.quit()
            exit()
        pass
