import pygame
import sys
import GIFImage
import time


class GUI:
    def __init__(self, _game_state):
        pygame.init()
        self.handler = None
        self.state = _game_state
        self.font_size = 30
        self.window_height = 600
        self.window_width = 600
        self.colors = {"white": (255, 255, 255),
                       "black": (41, 36, 33),
                       "navy": (0, 0, 128),
                       "red": (139, 0, 0),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "yellow": (255, 255, 0),
                       "turquoise blue": (0, 199, 140),
                       "green": (0, 128, 0),
                       "light green": (118, 238, 0),
                       "turquoise": (0, 229, 238),
                       "gray": (152, 152, 152),
                       "toolbar": (100,221,23),
                       "main_background": (118,255,3)}
        self.text_color = self.colors["red"]
        self.bg_color = self.colors["main_background"]
        self.tile_color = None
        self.tb_color = self.colors["toolbar"]
        self.shadow_color = (236,239,241)
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("League Search")
        self.loading_gif = GIFImage.GIFImage("assets/images/ring-alt.gif")
        self.button_sprites = pygame.image.load("assets\\images\\buttons.png")
        self.light_sprites = pygame.image.load("assets\\images\\leds.png")
        self.bg_sprites = pygame.image.load("assets\\images\\bg3.jpg")
        self.typing_tag = False

        # for setting up information for communication
        self.user_prompt = Prompt((self.window_width/4, self.window_height/3+100), self, "summoner name")

    def add_handler(self, handler):
        self.handler = handler

    def reset_prompts(self):
        self.user_prompt.reset()

    def make_text(self, text, color, bg_color, center, topleft=None, size=None):
        """
        Make a text object for drawing
        """
        if size:
            font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", size)
        else:
            font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if center:
            text_rect.center = center
        else:
            text_rect.topleft = topleft
        return text_surf, text_rect

    def set_typing_tag(self, val):
        """
        Decide whether you want to type or not.
        """
        self.typing_tag = val

    def draw_toolbar(self, title=True):
        pygame.draw.rect(self.display_surface, self.colors["toolbar"], pygame.Rect(0, 0, self.window_width,
                                                                                   self.window_height/6))
        self.display_surface.blit(self.bg_sprites, (0, 0))
        if title:
            title_sur, title_rect = self.make_text(self.state.get_state(), self.colors["blue"], self.tb_color, None,
                                                   (30, self.window_height/15))
            self.display_surface.blit(title_sur, title_rect)

    def draw_info(self, player, location):
        s = 22
        d = 20
        name_sur, name_rect = self.make_text(player[1], self.colors["turquoise"], self.bg_color, location, size=s)
        champ_sur, champ_rect = self.make_text(player[2], self.colors["red"], self.bg_color,
                                               (location[0], location[1]+d), size=s)
        win_sur, win_rect = self.make_text("Win rate: %.1f%%" % (player[3][0]*100), self.colors["dark"],
                                           self.bg_color, (location[0], location[1]+d*2), size=s)
        kda_sur, kda_rect = self.make_text("KDA: %.2f" % player[3][1], self.colors["dark"], self.bg_color,
                                           (location[0], location[1]+d*3), size=s)
        div_sur, div_rect = self.make_text(player[4], self.colors["blue"], self.bg_color,
                                           (location[0], location[1]+d*4), size=s)
        self.display_surface.blit(name_sur, name_rect)
        self.display_surface.blit(champ_sur, champ_rect)
        self.display_surface.blit(win_sur, win_rect)
        self.display_surface.blit(kda_sur, kda_rect)
        self.display_surface.blit(div_sur, div_rect)

    def draw(self, state):
        """
        Draw the scene.
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            start_point = 60
            self.new = Button('New Session', self.text_color, self.tile_color,
                              (self.window_width/2, start_point), self)
            self.quit = Button('Quit', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+120*3), self)
            self.help = Button('How to use this app', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+120), self)
            self.author = Button('About the author', self.text_color, self.tile_color,
                                 (self.window_width/2, start_point+120*2), self)
            self.buttons = [self.new, self.quit, self.help, self.author]
            self.display_surface.blit(self.new.get_sr()[0], self.new.get_sr()[1])
            self.display_surface.blit(self.quit.get_sr()[0], self.quit.get_sr()[1])
            self.display_surface.blit(self.help.get_sr()[0], self.help.get_sr()[1])
            self.display_surface.blit(self.author.get_sr()[0], self.author.get_sr()[1])

        elif state == "help":
            self.draw_toolbar()
            sys.stdin = open("assets/texts/instruction.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "author":
            self.draw_toolbar()
            sys.stdin = open("assets/texts/author.txt")
            for i in range(8):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "new session":
            self.draw_toolbar()
            self.user_prompt.draw_rect()
            self.save = Button("Go", self.text_color, self.tile_color, (4.5*self.window_width/5, self.window_height/4), self)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            choose_sur, choose_rect = self.make_text("Enter your summoner name", self.colors["green"], self.tile_color,
                                                     (self.window_width/2, self.window_height/4))
            self.buttons = [self.back, self.save]
            self.display_surface.blit(self.save.get_sr()[0], self.save.get_sr()[1])
            self.display_surface.blit(choose_sur, choose_rect)
            if self.typing_tag:
                self.display_surface.blit(self.user_prompt.output()[1], self.user_prompt.output()[2])
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            self.display_surface.blit(self.user_prompt.output_title()[0], self.user_prompt.output_title()[1])

        elif state == "player not found":
            self.draw_toolbar()
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            text_sur, text_rect = self.make_text("No summoner is found by this name!",
                                                 self.colors["green"], self.tile_color,
                                                 (self.window_width/2, self.window_height/2))
            self.buttons = [self.back]
            self.display_surface.blit(text_sur, text_rect)
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "player not in game":
            self.draw_toolbar()
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            text_sur, text_rect = self.make_text("This summoner is not in any game!",
                                                 self.colors["green"], self.tile_color,
                                                 (self.window_width/2, self.window_height/2))
            self.buttons = [self.back]
            self.display_surface.blit(text_sur, text_rect)
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "loading":
            self.loading_gif.render(self.display_surface, (self.window_width/2, self.window_height/2))
            text_sur, text_rect = self.make_text("Loading, please wait!",
                                                 self.colors["dark"], self.tile_color,
                                                 (self.window_width/2, 3*self.window_height/4))
            self.buttons = []
            self.display_surface.blit(text_sur, text_rect)

        elif state == "display info":
            self.draw_toolbar()
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back]
            location_blue = (80, 150)
            location_red = (80, 450)
            for p in self.handler.info:
                if p[0] == 100:
                    self.draw_info(p, location_blue)
                    location_blue = location_blue[0]+110, 150
                elif p[0] == 200:
                    self.draw_info(p, location_red)
                    location_red = location_red[0]+110, 450
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])


class Sprite:
    """
    Class for handling sprites
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui, dim=None):
        self.sheet = sheet
        self.loc_in_sheet = loc_in_sheet  # a dictionary keeping track of each movement and their sprites
        if dim:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["normal"][0], self.loc_in_sheet["normal"][1], dim[0], dim[1]))
            self.img = self.sheet.subsurface(self.sheet.get_clip())
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["normal"][0], self.loc_in_sheet["normal"][1], 50, 50))
            self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.pos = pos
        self.gui = _game_gui

    def get_img(self):
        return self.img

    def get_pos(self):
        return self.pos


class ButtonSprite(Sprite):
    """
    Child class for handling button sprites specifically
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 50)
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["hover"][0], self.loc_in_sheet["hover"][1], 50, 50))
        self.img_hover = self.sheet.subsurface(self.sheet.get_clip())
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["pressed"][0], self.loc_in_sheet["pressed"][1], 50, 50))
        self.img_pressed = self.sheet.subsurface(self.sheet.get_clip())

    def get_rect(self):
        return self.rect

    def set_pressed(self, pos):
        """
        Highlight the button when the user clicks mouse on
        """
        if self.rect.collidepoint(pos):
            self.gui.display_surface.blit(self.img_pressed, self.pos)

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.gui.display_surface.blit(self.img_hover, self.pos)


class LightSprite(Sprite):
    """
    Child class for handling light sprites specifically
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui, state):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui, (35, 35))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 35, 35)
        self.state = state
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["on"][0], self.loc_in_sheet["on"][1], 35, 35))
        self.img_on = self.sheet.subsurface(self.sheet.get_clip())

    def get_img(self):
        if self.state:
            return self.img_on
        else:
            return self.img

    def get_rect(self):
        return self.rect


class Button:
    """
    Class for handling buttons
    """
    def __init__(self, text, color, bg_color, center, _game_gui, topright=None):
        self.gui = _game_gui
        self.text = text
        self.topright = topright
        self.center = center
        self.color = color
        self.bg_color = bg_color
        self.bold = False
        self.font_size = 30
        font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.surf = font.render(text, True, color)
        self.rect = self.surf.get_rect()
        if self.center:
            self.rect.center = self.center
        else:
            self.rect.topright = self.topright

    def make_text(self):
        """
        Make a text object for drawing
        """
        if not self.bold:
            font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
            text_surf = font.render(self.text, True, self.color, self.bg_color)
        else:
            font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
            text_surf = font_bold.render(self.text, True, self.color)
        text_rect = text_surf.get_rect()
        if self.center:
            text_rect.center = self.center
        else:
            text_rect.topright = self.topright
        return text_surf, text_rect

    def get_rect(self):
        return self.rect

    def get_sr(self):
        return self.surf, self.rect

    def update_sr(self):
        self.surf, self.rect = self.make_text()

    def set_pressed(self, pos):
        pass

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.bold = True
            self.update_sr()
            self.gui.display_surface.blit(self.surf, self.rect)


class Prompt:
    """
    Prompt which takes input keyboard from user as a string
    """
    def __init__(self, topleft, _gui, title=""):
        self.title = title
        self.string = ""
        self.display_title = True
        self.gui = _gui
        self.colors = _gui.colors
        self.color = _gui.text_color
        self.bg_color = _gui.colors["white"]
        self.topleft = topleft
        self.font_size = 40
        self.rect = pygame.Rect(self.topleft[0], self.topleft[1], 360, 70)

    def draw_rect(self):
        """
        Draw a blank space
        :return:
        """
        if self.display_title:
            pygame.draw.rect(self.gui.display_surface, self.colors["white"], self.rect)
        else:
            pygame.draw.rect(self.gui.display_surface, self.colors["white"], self.rect, 3)

    def make_text(self, text, color=None):
        """
        Make a text object for drawing
        """
        font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        if color is None:
            if not self.display_title:
                text_surf = font.render(text, True, self.color)
            else:
                text_surf = font.render(text, True, self.color)
        else:
            text_surf = font.render(text, True, color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.topleft[0]+1, self.topleft[1]+3)
        return text_surf, text_rect

    def take_char(self, char):
        """
        Take in character or delete previous one.
        :return:
        """
        if char == "space":
            self.string += " "
        elif len(char) == 3:
            if int(char[1]) in range(10) and char[0] == "[" and char[2] == "]":
                self.string += char[1]
        elif char == "backspace":
            self.string = self.string[:-1]
        else:
            self.string += char

    def set_display_title(self):
        self.display_title = True

    def reset_display_title(self):
        self.display_title = False

    def output_title(self):
        """
        Output the title for this prompt
        :return:
        """
        if self.display_title and self.string == "":
            return self.make_text(self.title, self.colors["gray"])
        else:
            return self.make_text("", self.colors["gray"])

    def output(self):
        """
        Output the string
        :return:
        """
        sur, rect = self.make_text(self.string)
        return self.string, sur, rect

    def reset(self):
        """
        Reset the prompt
        :return:
        """
        self.string = ""
