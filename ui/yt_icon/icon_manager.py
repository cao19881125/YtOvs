from utils.singleton import singleton

@singleton
class IconManager(object):
    def __init__(self):
        self.__close_icons = {'red':'./icon/close/close_red.png',
                              'orange':'./icon/close/close_orange.png',
                              'yellow':'./icon/close/close_yellow.png',
                              'green':'./icon/close/close_green.png',
                              'blue':'./icon/close/close_blue.png',
                              'purple':'./icon/close/close_purple.png'}
        
        self.__label_icons = {'red':'./icon/label/label_red.png',
                              'orange':'./icon/label/label_orange.png',
                              'yellow':'./icon/label/label_yellow.png',
                              'green':'./icon/label/label_green.png',
                              'blue':'./icon/label/label_blue.png',
                              'purple':'./icon/label/label_purple.png'}


    def get_close_icons(self, color):
        return self.__close_icons[color]

    def get_label_icons(self, color):
        return self.__label_icons[color]