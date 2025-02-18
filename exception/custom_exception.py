class BadRequest(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'BadRequestError: {self.message} '
        else:
            return 'По вашему запросу ничего не найдено 😥'
