class Block:
    """
    A base class for blocks
    """
    def __init__(self, axis):
        pass

    def init(self):
        """
        initialize the animation.

        To be (optionally) implemented by subclasses
        """
        pass

    def update(self, i):
        """
        updates the block to display the corresponding frame i.

        To be implemented by subclasses
        """
        raise NotImplementedError()

    def __len__(self):
        """
        Returns the length of the 'time' axis
        """
        raise NotImplementedError()
