import pygame
import math

class XboxController:
    
    def __init__(self):
        pygame.init()
        self.steeringValue = 0.0
        self.throttleValue = 0.0
        self.breakValue = 0.0
        self.buttonA = 0
        self.joysticks = {}

    def getValues(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
        for joystick in self.joysticks.values():
            self.steeringValue = (joystick.get_axis(0)+1)*100-100
            self.throttleValue = (joystick.get_axis(5)+1)*50
            self.breakValue = (joystick.get_axis(4)+1)*50
            #print(f"{self.steeringValue:>6.1f}\t{self.throttleValue:>6.1f}\t{self.breakValue:>6.1f}")
            #print(f"{joystick.get_axis(0):>6.3f}\t{joystick.get_axis(5):>6.3f}\t{joystick.get_axis(4):>6.3f}")
            buttons = joystick.get_numbuttons()
        for i in range(buttons):
                button = joystick.get_button(i)
                if(i == 0):
                     self.buttonA = button
                else:
                     self.buttonA == button



        return round(self.steeringValue, 1), round(self.throttleValue, 1), round(self.breakValue, 1), self.buttonA
