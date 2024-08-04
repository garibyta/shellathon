class Argument:
    def __init__(self, *args, encoder=None, **kws):
        self.encoder = encoder or (lambda x: x)
        self.args = args
        self.kws = kws

        first_arg = self.args[0]
        self.orig_name = first_arg
        self.naked_name = self.orig_name.strip('-')
        self.placeholder_name = '{' + self.naked_name + '}'


class Rest:
    pass
