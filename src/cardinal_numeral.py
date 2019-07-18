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
    """
    Integer greater than 999,999,999,999
    """
    pass


def convert_units(n):
    """
    Return list cardinal numeral words from number of units.

    Parameters:
        n (int): n is a number from 0 to 9.

    Returns:
        cardinal_numberal_list (list): list of cardinal numeral words.
    """

    cardinal_numberal_list = []
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
    cardinal_numberal_list.append(switcher[n])

    return cardinal_numberal_list


def convert_tens(n):
    """
    Return list cardinal numeral words from number of tens.

    Parameters:
        n (int): n is a number from 10 to 99.

    Returns:
        cardinal_numberal_list (list): list of cardinal numeral words
    """

    cardinal_numberal_list = []

    # Converting digit of tens
    # In case digit is 1
    if n // 10 == 1:
        cardinal_numberal_list.append(NUMERAL_TEN1)
    # In case digit from 2 to 9
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
        cardinal_numberal_list.append(switcher[n // 10])
        cardinal_numberal_list.append(NUMERAL_TEN2)

    # Convert digit of units
    if n % 10 != 0:
        # Digit is from 2 to 9
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
            cardinal_numberal_list.append(switcher[n % 10])
        # Digit is 1
        else:
            if n // 10 == 1:
                cardinal_numberal_list.append(NUMERAL_ONE1)
            else:
                cardinal_numberal_list.append(NUMERAL_ONE2)

    return cardinal_numberal_list


def convert_hundreds(n, region = 'north'):
    """
    Return list cardinal numeral words from number of hundreds.

    Parameters:
        n (int): n is a number from 100 to 999, (can get value less than 100 to pronounce "khong tram").
        region (str): region is 'north' or 'south'.

    Returns:
        cardinal_numberal_list (list): list of cardinal numeral words.
    """

    reg = {'north': ONES1, 'south': ONES2}
    cardinal_numberal_list = []
    cardinal_numberal_list += convert_units(n // 100)
    cardinal_numberal_list.append(HUNDREDS)

    if n % 100 != 0:
        if n % 100 >= 10:
            cardinal_numberal_list += convert_tens(n % 100)
        else:
            cardinal_numberal_list.append(reg[region])
            cardinal_numberal_list += convert_units(n % 100)

    return cardinal_numberal_list


def integer_to_vietnamese_numeral(n, region = 'north', activate_tts = False):
    """
    Returns a string corresponding to Vietnamese cardinal numeral of a number.

    Parameters:
        n (int): n is a number from 0 to 999,999,999,999.
        region (str): region gets 'north' or 'south' to generate north or south Vietnamese cardinal numberal.
        activate_tts (bool): activate_tts gets True or False to say it or not.

    Returns:
        (str): a string corresponding to Vietnamese cardinal numeral of a number.
    """

    if (type(activate_tts) is not bool) and (type(activate_tts) is not None):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if activate_tts is None:
        activate_tts = False

    reg = {'north': THOUSANDS1, 'south': THOUSANDS2}
    if type(region) != str:
        raise TypeError('Argument "region" is not a string')
    if not region in reg:
        raise ValueError('Argument "region" has not a correct value')

    if type(n) is not int:
        raise TypeError("Not an integer")
    if n < 0:
        raise ValueError("Not a positive integer")
    if n > 999999999999:
        raise Overflow("Integer greater than 999,999,999,999")

    cardinal_numberal_list = []
    # Devide n to many set of three numbers
    list_divisor = (1000000000, 1000000, 1000, 1)
    for i in list_divisor:
        # If set of three numbers has any number is not zero
        if n // i > 0:
            # Saying if it is the first set of three numbers
            if len(cardinal_numberal_list) == 0:
                if n // i >= 100:
                    cardinal_numberal_list += convert_hundreds(n // i, region)
                elif n // i >= 10:
                    cardinal_numberal_list += convert_tens(n // i)
                else:
                    cardinal_numberal_list += convert_units(n // i)
            # Saying if it is NOT the first set of three numbers
            else:
                cardinal_numberal_list += convert_hundreds(n // i, region)

            # Adding place-value for set of three numbers
            if i == 1000000000:
                cardinal_numberal_list.append(BILLIONS)
            elif i == 1000000:
                cardinal_numberal_list.append(MILLIONS)
            elif i == 1000:
                cardinal_numberal_list.append(reg[region])

            # Removing set of three numbers converted
            n = n % i

    # Check activate_tts
    if not activate_tts:
        return ' '.join(cardinal_numberal_list)
    else:
        import pygame
        pygame.init()
        for word in cardinal_numberal_list:
            sound = pygame.mixer.Sound("../sounds/vie/" + str(region) + "/" + word + ".ogg")
            sound.play()
            print("../sounds/vie/" + str(region) + "/" + word + ".ogg")
            pygame.time.delay(600)
        return ' '.join(cardinal_numberal_list)


################################################################################################################


def convert_from_0_to_99(n):
    """
    Returns a string corresponding to a number between 0 and 99.
 
    Parameters:
        n (int): n is a number from 0 to 99.

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
        n (int): n is a number from 100 to 999.

    Returns:
        cardinal_numberal_list (list): a list of words corresponding to English cardinal numeral of a number.
    """

    cardinal_numberal_list = []

    if n < 100:
        cardinal_numberal_list.append(convert_from_0_to_99(n))
    else:
        cardinal_numberal_list.append(convert_from_0_to_99(n // 100))
        cardinal_numberal_list.append("hundred")

        if n % 100 != 0:
            cardinal_numberal_list.append("and")
            cardinal_numberal_list.append(convert_from_0_to_99(n % 100))

    return cardinal_numberal_list


def integer_to_english_numeral(n, activate_tts = False):
    """
    Returns a string corresponding to the English cardinal numeral of this number. 

    Parameters:
        n (int): n is a number.
        activate_tts (bool): True with sound, False without sound.

    Returns:
        cardinal_numberal_list (list): a list of words corresponding to English cardinal numeral of a number.
    """

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

    cardinal_numberal_list = []
    # Devide n to many set of three numbers
    list_divisor = (1000000000, 1000000, 1000, 1)
    for i in list_divisor:
        # If set of three numbers has any number is not zero
        if n // i > 0:
            cardinal_numberal_list += convert_hundreds_en(n // i)

            # Adding place-value for set of three numbers
            if i == 1000000000:
                cardinal_numberal_list.append("billion")
            elif i == 1000000:
                cardinal_numberal_list.append("million")
            elif i == 1000:
                cardinal_numberal_list.append("thousand")

            if n % i != 0:
                cardinal_numberal_list.append("and")

            # Removing set of three numbers converted
            n = n % i

    if not activate_tts:
        return ' '.join(cardinal_numberal_list)
    else:
        import pygame
        pygame.init()
        for word in cardinal_numberal_list:
            if word.find('-') == -1:
                sound = pygame.mixer.Sound("../sounds/en/" + word + ".ogg")
                sound.play()
                print("../sounds/en/" + word + ".ogg")
                pygame.time.delay(600)
            else:
                sound = pygame.mixer.Sound("../sounds/en/" + word[: word.find('-')] + ".ogg")
                sound.play()
                print("../sounds/en/" + word[0 : word.find('-')] + ".ogg")
                pygame.time.delay(600)

                sound = pygame.mixer.Sound("../sounds/en/" + word[word.find('-') + 1 :] + ".ogg")
                sound.play()
                print("../sounds/en/" + word[word.find('-') + 1 :] + ".ogg")
                pygame.time.delay(600)

        return ' '.join(cardinal_numberal_list)
