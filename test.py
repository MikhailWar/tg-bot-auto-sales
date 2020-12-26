

class message:
    text="кор"


_name_item = message.text[1:]
first_letter = message.text[:1].upper()
name_item = first_letter +_name_item
print(name_item)