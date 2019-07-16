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


def convert_units(n):
    """
    Return list cardinal numeral words from number of units.

    Parameters:
    n (int): n is a number between 1 and 9.

    Returns:
    res (list): res has 1 element, pronounce a number between 1 and 9.
    """

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


def convert_tens(n):
    res = []
    """
    Return list cardinal numeral words from number of tens.

    Parameters:
    n (int): n is a number between 10 and 99.

    Returns:
    res (list): res have many element, pronounce a number between 10 and 99.
    """

    if n // 10 == 1:
        res.append(NUMERAL_TEN1)
    # n from 2x to 9x
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
    # n % 10 != 0, so digit of units is from 1 to 9
    if n % 10 != 0:
        # n % 10 != 1, so digit of units is from 2 to 9
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
        # In this case, the digit is definitely 1, một or mốt
        else:
            if n // 10 == 1:
                res.append(NUMERAL_ONE1)
            else:
                res.append(NUMERAL_ONE2)
    return res


def convert_hundreds(n, region = 'north'):
    """
    Return list cardinal numeral words from number of hundreds.

    Parameters:
    n (int): n is a number between 100 and 999, (can get value less than 100 to pronounce "khong tram").
    region (str): region is 'north' or 'south'.

    Returns:
    res (list): res have many element, pronounce a number between 100 and 999 (or less than 100 to pronounce "khong tram").
    """

    # waypoint 2, linh in north, lẻ in south
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
    """
    Returns a string corresponding to Vietnamese cardinal numeral of a number.

    Parameters:
    n (int): n is a number maximum 999,999,999,999.
    region (str): region is 'north' or 'south'.
    activate_tts (bool): True with sound, False without sound.

    Returns:
    res (str): a string corresponding to Vietnamese cardinal numeral of a number.
    """

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
    """
    Returns a string corresponding to a number between 0 and 99.
 
    Parameters:
    n (int): n is a number between 0 and 99.

    Returns:
    res (str): a string corresponding to English cardinal numeral of a number.
    """

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
    """
    Returns a string corresponding to a number between 100 and 999.
 
    Parameters:
    n (int): n is a number between 100 and 999.

    Returns:
    res (list): a list of string corresponding to English cardinal numeral of a number.
    """

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


<<<<<<< HEAD
def integer_to_english_numeral(n, activate_tts = False):
=======
def integer_to_english_numeral(n):
    """
    Returns a string corresponding to the English cardinal numeral of this number. 

    Parameters:
    n (int): n is a number.
    activate_tts (bool): True with sound, False without sound.

    Returns:
    res (str): a string corresponding to English cardinal numeral of a number.
    """

>>>>>>> document_code
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
