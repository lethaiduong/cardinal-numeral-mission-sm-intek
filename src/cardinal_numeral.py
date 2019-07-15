# User defined custom exception
class Overflow(Exception):
    """Integer greater than 999,999,999,999"""
    pass


# Return list cardinal numeral words from number of units
def units(n):
    res = []
    switcher = {
            0: "không",
            1: "một",
            2: "hai",
            3: "ba",
            4: "bốn",
            5: "năm",
            6: "sáu",
            7: "bảy",
            8: "tám",
            9: "chín"
    }
    res.append(switcher[n])
    return res


# Return list cardinal numeral words from number of dozens
def dozens(n):
    res = []

    # Convert digit of dozens
    if n // 10 == 1:
        res.append("mười")
    else:
        switcher = {
                2: "hai",
                3: "ba",
                4: "bốn",
                5: "năm",
                6: "sáu",
                7: "bảy",
                8: "tám",
                9: "chín"
        }
        res.append(switcher[n // 10])
        res.append("mươi")

    # Convert digit of units
    if n % 10 != 0:
        if n % 10 != 1:
            switcher = {
                    2: "hai",
                    3: "ba",
                    4: "bốn",
                    5: "lăm",
                    6: "sáu",
                    7: "bảy",
                    8: "tám",
                    9: "chín"
            }
            res.append(switcher[n % 10])
        else:
            if n // 10 == 1:
                res.append("một")
            else:
                res.append("mốt")
    return res


# Return list cardinal numeral words from number of hundreds
def hundreds(n):
    res = []
    res = res + units(n // 100)
    res.append("trăm")

    if n % 100 != 0:
        if n % 100 >= 10:
            res = res + dozens(n % 100)
        else:
            res.append("linh")
            res = res + units(n % 100)
    return res


# Waypoint 1
def integer_to_vietnamese_numeral(n):
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
                    res = res + hundreds(n // i)
                elif n // i >= 10:
                    res = res + dozens(n // i)
                else:
                    res = res + units(n // i)
            else:
                res = res + hundreds(n // i)

            if i == 1000000000:
                res.append("tỷ")
            elif i == 1000000:
                res.append("triệu")
            elif i == 1000:
                res.append("nghìn")

            n = n % i

    return res
