class Buttons():
    def __init__(self, image, x_pos, y_pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.image_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.image_rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else: self.text = self.font.render(self.text_input, True, self.base_color)

            
