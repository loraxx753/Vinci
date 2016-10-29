import os, time, sys

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor


class Vinci:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    DEFAULT_INDENT = 4
    DEFAULT_INDENT_CHARACTER = " "

    _clear_options = []

    def __init__(self, debug=False, show=True):
        raw_width, raw_height = os.popen('stty size', 'r').read().split()
        self.width = int(raw_width)
        self.height = int(raw_height)
        self.debug = debug
        self.show = show

        self.rows = self.width
        self.cols = self.height

        # self.current_location = self._update_position()
        self._line_numbers = []
        self._lines = {}
        self._time_start = datetime.now()
        self.rebuild_lines()

    def rebuild_lines(self):
        for x in range(self.rows):
            self._lines['line_{}'.format(x)] = ''
            self._line_numbers.append('line_{}'.format(x))

    def move_up(self, lines, start=False):
        self._execute(lines, 'A')
        if start:
            self._execute(lines, 'A')
        else:
            self._execute(lines, 'F')

    def move_down(self, lines, start=False):
        if start:
            self._execute(lines, 'B')
        else:
            self._execute(lines, 'E')

    def move_forward(self, columns):
        self._execute(columns, 'C')

    def move_backward(self, columns):
            self._execute(columns, 'D')

    def move_to(self, column: int=0, line: int=0, ) -> None:
        if not column:
            self._execute("{0};{1}".format(line, column), 'f')
        elif not line:
            self._execute(column, 'G')
        else:
            self._execute("{0};{1}".format(line, column), 'f')
    """
        See https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    def clear(self, out='all', origin=(None,None)):
        origin = (0, 0) if out == 'all' and origin == (None, None) else origin

        self.move_to(0, 0)
        for i in range(1, self.height):
            self.clear_line(whole_line=2)
            self.move_down(1)

        if origin != (None, None):
            self.move_to(*origin)

    def clear_line(self, whole_line=1) -> None:
        self._execute(whole_line, 'K')

    def save(self) -> None:
        self._execute('s')

    def restore(self) -> None:
        self._execute('u')

    def update_line(self, line: int, template_text: str, *args, indent: int=False, print_line=True, **kwargs):
        if indent:
            indent_string = self.DEFAULT_INDENT_CHARACTER * self.DEFAULT_INDENT
            template_text = indent_string + template_text

        self._lines['line_{}'.format(line)] = template_text

        if print_line:
            self.clear()
            self.print_lines()

        # FO' LATER ===========================================================
        # if name not in self._line_numbers:
        #     if row > -1:
        #         self._line_numbers.insert(row, name)
        #     else:
        #         self._line_numbers.append(name)
        #     self._lines.update({name: template_text.format(*args, **kwargs)})
        # else:
        #     raise ValueError('The key {} already appears in the list at line #{}'.format(
        #         name,
        #         self._line_numbers.index(name)
        #     ))

    def reset(self):
        self.clear()
        self.rebuild_lines()

    def hide_cursor(self):
        self._execute("?25", "l")

    def show_cursor(self):
        self._execute("?25", "h")

    def get_lines(self):
        return len(self._line_numbers)

    def get_line(self, key: any) -> str:
        if type(key) == int:
            output = self._lines[key - 1] if key < len(self._line_numbers) else ''
        elif type(key) == str:
            output = self._lines[key] if key in self._lines else ''
        else:
            raise TypeError("key must be an instance of int or str")
        return output

    def is_line(self, key: any) -> bool:
        if type(key) == int:
            return True if key < len(self._line_numbers) else False
        elif type(key) == str:
            return True if key in self._lines else False
        else:
            raise TypeError("key must be an instance of int or str")

    def _update_position(self):
        return self.save()

    def replace_line(self, header_name: str, new_text: str = '', *args, **kwargs):
        self._lines[header_name] = new_text.format(*args, **kwargs)

    def print_lines(self):
        for key in self._line_numbers:
            line_num = int(key.split('_').pop(-1))
            self.move_to(1, line_num)
            if self._lines[key]:
                if self.debug:
                    text = self.RED + self.BOLD + key + "({:,}): ".format(line_num) + self.END +self._lines[key]
                else:
                    text = self._lines[key]
                self.clear_line()
                self.print_line(text)

    def print_line(self, line_text: str='') -> None:
        if line_text and self.show:
            print(line_text)

    def _execute(self, *args):
        if len(args) > 0:
            syntax = "{}" * len(args)
            print("\033[" + syntax.format(*args), end="\r")
        else:
            raise ValueError("You have to supply a number and letter in this form: self._execute(columns, 'D')")