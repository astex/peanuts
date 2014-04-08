import bcrypt

class Password(object):
    """Password convenience class.

        Hash passwords like `pw = Password.hashpw(password)`.  Create an instance from a hashed password by
        initializing with the hash.  Compare it to passwords like `pw == password`.
    """

    def __init__(self, hashed): self.hashed = hashed
    def __eq__(self, pw): return bcrypt.hashpw( pw.encode('utf-8'), self.hashed.encode('utf-8') ) == self.hashed

    @classmethod
    def hashpw(cls, pw): return cls( bcrypt.hashpw( pw.encode('utf-8'), bcrypt.gensalt() ) )
