# Defined numbers
NUMERAL_ZERO    =   "không"
NUMERAL_ONE1    =   "một"
NUMERAL_ONE2    =   "mốt"
NUMERAL_TWO     =   "hai"
NUMERAL_THREE   =   "ba"
NUMERAL_FOUR    =   "bốn"
NUMERAL_FIVE1   =   "năm"
NUMERAL_FIVE2   =   "lăm"
NUMERAL_SIX     =   "sáu"
NUMERAL_SEVEN   =   "bảy"
NUMERAL_EIGHT   =   "tám"
NUMERAL_NINE    =   "chín"
NUMERAL_TEN1    =   "mười"
NUMERAL_TEN2    =   "mươi"
ONES1           =   "linh"
ONES2           =   "lẻ"
HUNDREDS        =   "trăm"
THOUSANDS1      =   "nghìn"
THOUSANDS2      =   "ngàn"
MILLIONS        =   "triệu"
BILLIONS        =   "tỷ"

# User defined custom exception
class Overflow(Exception):
    """Integer greater than 999,999,999,999"""
    pass


# Return list cardinal numeral words from number of units
def convert_units(n):
    res = []
    switcher = {
            0: NUMERAL_ZERO,
            1: NUMERAL_ONE1,
            2: NUMERAL_TWO,
            3: NUMERAL_THREE,
            4: NUMERAL_FOUR,
            5: NUMERAL_FIVE1,
            6: NUMERAL_SIX,
            7: NUMERAL_SEVEN,
            8: NUMERAL_EIGHT,
            9: NUMERAL_NINE
    }
    res.append(switcher[n])
    return res


# Return list cardinal numeral words from number of tens
def convert_tens(n):
    res = []

    # Convert digit of tens
    if n // 10 == 1:
        res.append(NUMERAL_TEN1)
    else:
        switcher = {
                2: NUMERAL_TWO,
                3: NUMERAL_THREE,
                4: NUMERAL_FOUR,
                5: NUMERAL_FIVE1,
                6: NUMERAL_SIX,
                7: NUMERAL_SEVEN,
                8: NUMERAL_EIGHT,
                9: NUMERAL_NINE
        }
        res.append(switcher[n // 10])
        res.append(NUMERAL_TEN2)

    # Convert digit of units
    if n % 10 != 0:
        if n % 10 != 1:
            switcher = {
                    2: NUMERAL_TWO,
                    3: NUMERAL_THREE,
                    4: NUMERAL_FOUR,
                    5: NUMERAL_FIVE2,
                    6: NUMERAL_SIX,
                    7: NUMERAL_SEVEN,
                    8: NUMERAL_EIGHT,
                    9: NUMERAL_NINE
            }
            res.append(switcher[n % 10])
        else:
            if n // 10 == 1:
                res.append(NUMERAL_ONE1)
            else:
                res.append(NUMERAL_ONE2)
    return res


# Return list cardinal numeral words from number of hundreds
def convert_hundreds(n, region = 'north'):
    reg = {'north': ONES1, 'south': ONES2}
    res = []
    res = res + convert_units(n // 100)
    res.append(HUNDREDS)

    if n % 100 != 0:
        if n % 100 >= 10:
            res = res + convert_tens(n % 100)
        else:
            res.append(reg[region])
            res = res + convert_units(n % 100)
    return res


# Waypoint 1
def integer_to_vietnamese_numeral(n, region = 'north', activate_tts = False):
    reg = {'north': THOUSANDS1, 'south': THOUSANDS2}
    if (type(activate_tts) is not bool) and (type(activate_tts) is not None):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if activate_tts is None:
        activate_tts = False
    if type(region) != str:
        raise TypeError('Argument "region" is not a string')
    if not region in reg:
        raise ValueError('Argument "region" has not a correct value')

    res = []
    # Catch exceptions
    if type(n) is not int:
        raise TypeError("Not an integer")
    if n < 0:
        raise ValueError("Not a positive integer")
    if n > 999999999999:
        raise Overflow("Integer greater than 999,999,999,999")

    list_divisor = (1000000000, 1000000, 1000, 1)
    for i in list_divisor:
        if n // i > 0:
            if len(res) == 0:
                if n // i >= 100:
                    res = res + convert_hundreds(n // i, region)
                elif n // i >= 10:
                    res = res + convert_tens(n // i)
                else:
                    res = res + convert_units(n // i)
            else:
                res = res + convert_hundreds(n // i, region)

            if i == 1000000000:
                res.append(BILLIONS)
            elif i == 1000000:
                res.append(MILLIONS)
            elif i == 1000:
                res.append(reg[region])

            n = n % i

    if not activate_tts:
        return ' '.join(res)
    else:
        import pygame
        pygame.init()
        for word in res:
            sound = pygame.mixer.Sound("../sounds/vie/" + str(region) + "/" + word + ".ogg")
            sound.play(maxtime = 3000)
            print("../sounds/vie/" + str(region) + "/" + word + ".ogg")
            pygame.time.delay(500)
        return ' '.join(res)

##################################################################

def convert_from_0_to_99(n):
    if n < 20:
        switcher = {
                0: "zero",
                1: "one",
                2: "two",
                3: "three",
                4: "four",
                5: "five",
                6: "six",
                7: "seven",
                8: "eight",
                9: "nine",
                10: "ten",
                11: "eleven",
                12: "twelve",
                13: "thirteen",
                14: "fourteen",
                15: "fifteen",
                16: "sixteen",
                17: "seventeen",
                18: "eighteen",
                19: "nineteen"
        }
        return switcher[n]
    else:
        switcher = {
                2: "twenty",
                3: "thirty",
                4: "forty",
                5: "fifty",
                6: "sixty",
                7: "seventy",
                8: "eighty",
                9: "ninety"
        }

        if n % 10 == 0:
            res = switcher[n // 10]
        else:
            res = switcher[n // 10] + "-" + convert_from_0_to_99(n % 10)

        return res


def convert_hundreds_en(n):
    res = []

    if n < 100:
        res.append(convert_from_0_to_99(n))
    else:
        res.append(convert_from_0_to_99(n // 100))
        res.append("hundred")

        if n % 100 != 0:
            res.append("and")
            res.append(convert_from_0_to_99(n % 100))

    return res


def integer_to_english_numeral(n, activate_tts = False):
    if type(n) is not int:
        raise TypeError("Not an integer")
    if n < 0:
        raise ValueError("Not a positive integer")
    if n > 999999999999:
        raise Overflow("Integer greater than 999,999,999,999")

    if (type(activate_tts) is not bool) and (type(activate_tts) is not None):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if activate_tts is None:
        activate_tts = False

    res = []
    list_divisor = (1000000000, 1000000, 1000, 1)
    for i in list_divisor:
        if n // i > 0:
            res = res + convert_hundreds_en(n // i)

            if i == 1000000000:
                res.append("billion")
            elif i == 1000000:
                res.append("million")
            elif i == 1000:
                res.append("thousand")

            if n % i != 0:
                res.append("and")

            n = n % i

    if not activate_tts:
        return ' '.join(res)
    else:
        # import pygame
        # pygame.init()
        for word in res:
            if word.find('-') == -1:
                # sound = pygame.mixer.Sound("../sounds/en/" + word + ".ogg")
                # sound.play(maxtime = 3000)
                print("../sounds/en/" + word + ".ogg")
                # pygame.time.delay(500)
            else:
                # sound = pygame.mixer.Sound("../sounds/en/" + word[: word.find('-')] + ".ogg")
                # sound.play(maxtime = 3000)
                print("../sounds/en/" + word[0 : word.find('-')] + ".ogg")
                # pygame.time.delay(500)

                # sound = pygame.mixer.Sound("../sounds/en/" + word[word.find('-') + 1 :] + ".ogg")
                # sound.play(maxtime = 3000)
                print("../sounds/en/" + word[word.find('-') + 1 :] + ".ogg")
                # pygame.time.delay(500)

        return ' '.join(res)