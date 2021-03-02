from mycroft import MycroftSkill, intent_file_handler


class GameOfLife(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('life.of.game.intent')
    def handle_life_of_game(self, message):
        self.speak_dialog('life.of.game')


def create_skill():
    return GameOfLife()

