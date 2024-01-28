class User:
    __Surname = None
    __Firstname = None
    __Middlename = None
    __AccessCode = None

    def __init__(self, Surname, Firstname, Middlename, AccessCode):
        self.Surname = Surname
        self.Firstname = Firstname
        self.Middlename = Middlename
        self.AccessCode = AccessCode
