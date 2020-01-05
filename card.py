class CARD(object):
    def __init__(self, color, number, is_show):
        self._color = color
        self._number = number
        self._is_show = is_show

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    @property
    def is_show(self):
        return self._is_show

    @is_show.setter
    def is_show(self, var):
        self._is_show = var

