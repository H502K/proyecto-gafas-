from machine import Pin, I2C
import ssd1306

#
i2c = I2C(0, scl=Pin(12), sda=Pin(13))


oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def print_to_oled(text):
    oled.fill(0)  
    oled.text(text, 0, 0)  
    oled.show()  

class Menu:
    def __init__(self, output_function=print_to_oled):
        self.items = []
        self.index = 0
        self.max_items = 10
        self.num_items = 0
        self.output_function = output_function
        
    def enter(self):
        action = self.items[self.index]['action']
        if action is not None:
            action()
        
    def Up(self):
        if self.index < (self.num_items - 1):     
            self.index += 1
            self.display_current_option()

    def down(self):
        if self.index > 0:                 
            self.index -= 1
            self.display_current_option()

    def add_item(self, text, action):
        if self.num_items < self.max_items:
            self.items.append({'text': text, 'action': action})
            self.num_items += 1

    def display_current_option(self):
        current_option = self.items[self.index]['text']
        self.output_function(current_option)
        
        print(current_option)

    def print_menu(self):
        for item in self.items:
            self.output_function(item['text'])


oled_menu = Menu()
