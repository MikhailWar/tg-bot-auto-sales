

class ErrorFormat(Exception):
    pass


def parse_amount(message) -> str:
    amount = None
    if message.isdigit():  # ловит обычное число в формате 1000, 10.10
        print("dsdsda")
        amount = "{:_}".format(int(message))
        return amount

    find_comma = message.find(",")
    find_space = message.find(" ")
    find_point = message.find(".")

    if find_point > -1:
        amount = message

    elif find_space > -1:
        amount = message.replace(' ', "")

    elif find_comma > -1:
        amount = message.replace(",", "")  # получаем # на выходе 10.000
        amount = "{:_}".format(int(amount))
    else:
        raise ErrorFormat

    return amount


