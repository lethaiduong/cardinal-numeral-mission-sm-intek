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
def convert_hundreds(n):
    res = []
    res = res + convert_units(n // 100)
    res.append(HUNDREDS)

    if n % 100 != 0:
        if n % 100 >= 10:
            res = res + convert_tens(n % 100)
        else:
            res.append(ONES1)
            res = res + convert_units(n % 100)
    return res


# Waypoint 1
def integer_to_vietnamese_numeral(n, activate_tts = False):
    if (type(activate_tts) is not bool) and (type(activate_tts) is not None):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if activate_tts is None:
        activate_tts = False

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
                    res = res + convert_hundreds(n // i)
                elif n // i >= 10:
                    res = res + convert_tens(n // i)
                else:
                    res = res + convert_units(n // i)
            else:
                res = res + convert_hundreds(n // i)

            if i == 1000000000:
                res.append(BILLIONS)
            elif i == 1000000:
                res.append(MILLIONS)
            elif i == 1000:
                res.append(THOUSANDS1)

            n = n % i

    if not activate_tts:
        return res
    else:
        import pygame
        pygame.init()
        for word in res:
            sound = pygame.mixer.Sound("../sounds/vie/north/" + word + ".ogg")
            sound.play(maxtime = 2200)
            print("../sounds/vie/north/" + word + ".ogg")
            pygame.time.delay(400)
        return res

##################################################################