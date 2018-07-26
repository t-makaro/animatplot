from .base import Block


class Line(Block):
    def __init__(self, x, y, axis=None):
        if x.shape != y.shape:
            raise "x, y must be the same shape"
        self.x = x
        self.y = y
        self.ax = axis

    def init(self):
        self.line, = self.ax.plot(self.x[:, 0], self.y[:, 0])

    def update(self, i):
        x_vector = self.x[i, :]
        y_vector = self.y[i, :]

        self.line.set_data(x_vector, y_vector)
        return self.line

    def __len__(self):
        return self.x.shape[0]
