import pygame
import sys
from pygame.locals import *
import core_communication
from multiprocessing import Queue, Process


def api_call_process(queue, playerId):
    communicator = core_communication.WebServerCommunication()
    info = communicator.getCurrentGame(playerId)
    print info
    queue.put(info)


class EventLogic:
    def __init__(self, _game_state, _game_gui):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self.communicator = core_communication.WebServerCommunication()
        self.current_prompt = None
        self.info = None
        self.queue = Queue()

    def quit(self):
        pygame.quit()
        sys.exit()

    def check_queue(self):
        if not self.queue.empty():
            info = self.queue.get()
            if info == "not in game":
                self._game_state.set_state("player not in game")
            else:
                self._game_state.set_state("display info")
                self.info = info


    def event_handler(self):
        event = pygame.event.poll()
        self.check_queue()
        if event.type == MOUSEBUTTONDOWN:
            if self._game_gui.buttons:
                for button1 in self._game_gui.buttons:
                    button1.set_pressed(pygame.mouse.get_pos())

            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new session")
                elif self._game_gui.help.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("help")
                elif self._game_gui.author.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("author")
                elif self._game_gui.quit.get_rect().collidepoint(event.pos):
                    self.quit()

            elif self._game_state.get_state() == "new session":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                elif self._game_gui.user_prompt.rect.collidepoint(event.pos):
                    self._game_gui.set_typing_tag(True)
                    self._game_gui.user_prompt.reset_display_title()
                    self.current_prompt = self._game_gui.user_prompt
                elif self._game_gui.save.get_rect().collidepoint(event.pos):
                    name = self._game_gui.user_prompt.output()[0]
                    Id = self.communicator.getPlayerIdByName(name)
                    if Id == "not found":
                        self._game_state.set_state("player not found")
                    else:
                        apiCaller = Process(target=api_call_process, args=(self.queue, Id))
                        apiCaller.start()
                        self._game_state.set_state("loading")
                    self._game_gui.reset_prompts()
                else:
                    self._game_gui.set_typing_tag(False)

            elif self._game_state.get_state() == "display info":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new session")
                    self._game_gui.user_prompt.set_display_title()

            elif self._game_state.get_state() == "player not found":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new session")
                    self._game_gui.user_prompt.set_display_title()

            elif self._game_state.get_state() == "player not in game":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new session")
                    self._game_gui.user_prompt.set_display_title()

            elif self._game_state.get_state().find("error") != -1:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")

            elif self._game_state.get_state() in ["help", "author", "settings"]:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            if self._game_gui.buttons:
                for button in self._game_gui.buttons:
                    button.set_bold(pygame.mouse.get_pos())

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.quit()

            else:
                if self._game_gui.typing_tag:
                    self.current_prompt.take_char(pygame.key.name(event.key))
