class SnoodRand:

    def __init__(self):
        # A 800-bit state, baby! Snood has only the best!
        # Much better than any 32-bit seeds!
        self.__state = [0] * 25

        # But that's not all, it's actually a 804-bit state! 
        # We throw an extra number into the calculation!
        # Amazing!
        self.__count = 0

        # And hold on; I'll double that offer -- here's some extra unchanging state you can have
        # Free!
        self.__static_state = [0, 0x8EBFD028]

        self.srand()

    # 08003A50
    def srand(self):
        # Random numbers generated fairly by 4294967296-sided die
        self.__state[0] = 0x95F24DAB
        self.__state[1] = 0xB685215
        self.__state[2] = 0xE76CCAE7
        self.__state[3] = 0xAF3EC239
        self.__state[4] = 0x715FAD23
        self.__state[5] = 0x24A590AD
        self.__state[6] = 0x69E4B5EF
        self.__state[7] = 0xBF456141
        self.__state[8] = 0x96BC1B7B
        self.__state[9] = 0xA7BDF825
        self.__state[10] = 0xC1DE75B7
        self.__state[11] = 0x8858A9C9
        self.__state[12] = 0x2DA87693
        self.__state[13] = 0xB657F9DD
        self.__state[14] = 0xFFDC8A9F
        self.__state[15] = 0x8121DA71
        self.__state[16] = 0x8B823ECB
        self.__state[17] = 0x885D05F5
        self.__state[18] = 0x4E20CD47
        self.__state[19] = 0x5A9AD5D9
        self.__state[20] = 0x512C0C03
        self.__state[21] = 0xEA857CCD
        self.__state[22] = 0x4CC1D30F
        self.__state[23] = 0x8891A8A1
        self.__state[24] = 0xA6B7AADB

        # We don't reset __count here but this function is only called by the game init code so it'd just be 0 anyways 

        # Now that we filled up state, we're going to do a little move that only the devs
        # of Snood could make up. We're gonna make state more random by running our deterministic
        # rand function on our deterministic inputs. Genius!
        n = int(self.rand() * 10000.0) % 50 # returns 30

        for _ in range(n):
            self.rand()

    # 8003B54
    def rand(self) -> float:
        # Returns a double from [0..1]. That's right, a double! Snood is so well-programmed
        # it can handle doubles even on the GBA, and we're going to use the best data type available!

        if self.__count == 25:
            for i in range(17 + 1):
                a = self.__state[i]
                b = self.__state[i + 7]
                b ^= (a >> 1)
                a &= 1
                b ^= self.__static_state[a]
                self.__state[i] = b

            for i in range(18, 24 + 1):
                a = self.__state[i]
                b = self.__state[i - 18]
                b ^= (a >> 1)
                a &= 1
                b ^= self.__static_state[a]
                self.__state[i] = b

            self.__count = 0

        a = self.__state[self.__count]
        a ^= (a << 7) & 0x2B5B2500
        a ^= (a << 15) & 0xDB8B0000
        a ^= (a >> 16)

        # (Python bigint to 32-bit int)
        a &= 0xFFFF_FFFF

        self.__count += 1

        # This should recreate int_to_double in Python
        sign = (a & 0x8000_0000) != 0
        if sign:
            a = -((2**32) - a)
        a = float(a)
        
        # Now we convert the double with int32 range to our [0..1] range
        if a < 0:
            a += (2**32)
        a /= (2**32) - 1
        
        return a


# Create a snood random instance
snood_rand = SnoodRand()

# And print out the first 50 random numbers we expect the game to generate
# (after srand is called, of course)
for i in range(50):
    print(f"rand() call {i}: {snood_rand.rand()}")
