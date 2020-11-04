class Player:

    def __init__(self, *args):

        '''Player constructor:
        Args:
        lastName (string)
        firstName (string)
        tierScore (int)
        tier (string)
        - Any other parameters will be ignored
        '''

        self.__lastName = args[0]

        self.__firstName = args[1]

        self.__tierScore = args[2]

        self.__tier = args[3]

    def getTier(self):

        '''
        getTier(self)
        Args: void
        Returns: tier (string)
        '''

        return self.__tier

    def getTierScore(self):

        '''
        getTierScore(self)
        Args: void
        Returns: tierScore (int)
        '''

        return self.__tierScore

    def getFirstName(self):

        '''
        getFirstName(self)
        Args: void
        Returns: firstName (string)
        '''

        return self.__firstName

    def getLastName(self):

        '''
        getLastName(self)
        Args: void
        Returns: lastName (string)
        '''

        return self.__lastName

    def setTier(self, strTier):

        '''
        setTier(self)
        Args: strTier (string)
        Returns: void
        - Changes self.__tier to args provided
        '''

        self.__tier = strTier

    def setTierScore(self, intTierScore):

        '''
        setTierScore(self)
        Args: intTierScore (integer)
        Returns: void
        - Changes self.__tierScore to args provided
        '''

        self.__tierScore = intTierScore

    def setFirstName(self, strFirstName):

        '''
        setFirstName(self)
        Args: strFirstName (string)
        Returns: void
        - Changes self.__firstName to args provided
        '''

        self.__firstName = strFirstName

    def setLastName(self, strLastName):

        '''
        setLastName(self)
        Args: strLastName (string)
        Returns: void
        - Changes self.__lastName to args provided
        '''

        self.__lastName = strLastName




