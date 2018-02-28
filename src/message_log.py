from bearlibterminal import terminal as blt
from collections import deque, namedtuple, Sequence


Message = namedtuple('Message', ['text', 'color', 'lines'])


class MessageLog(Sequence):
    """Message log with a buffer."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.messages = deque([])
        self.lines = 0

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    def add_message(self, message, color='white'):
        """Add message to log.

        Wraps messages to width and deletes lines when buffer is full.
        """
        _, num_lines = blt.measure(message, self.width, self.height)
        self.lines += num_lines
        while self.lines >= self.height:
            oldest_message = self.messages.popleft()
            self.lines -= oldest_message.lines
        self.messages.append(
            Message(text=message, color=color, lines=num_lines))
