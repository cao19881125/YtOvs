import os
from utils.singleton import singleton
ICON_IDR = os.path.join(os.path.dirname(__file__),'../../icon/')

@singleton
class IconManager(object):
    def __init__(self):
        self.__close_icons = {'red':'close_red.png',
                              'orange':'close_orange.png',
                              'yellow':'close_yellow.png',
                              'green':'close_green.png',
                              'blue':'close_blue.png',
                              'purple':'close_purple.png'}
        
        self.__label_icons = {'red':'label_red.png',
                              'orange':'label_orange.png',
                              'yellow':'label_yellow.png',
                              'green':'label_green.png',
                              'blue':'label_blue.png',
                              'purple':'label_purple.png'}


    def get_close_icons(self, color):
        return ICON_IDR + 'close/' + self.__close_icons[color]

    def get_label_icons(self, color):
        return ICON_IDR + 'label/' + self.__label_icons[color]