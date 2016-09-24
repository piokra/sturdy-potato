class Generator:
    """ A value generator """

    def __init__(self):
        raise NotImplementedError('This is an abstract method')

    def get(self):
        """
        Generates next value
        :return: Next Value
        """
        raise NotImplementedError('This is an abstract method')

    def range(self, n):
        """
        Generates a range of values
        :param n: Number of values
        :return: A sequence of values
        """
        for i in range(n):
            yield self.get()
