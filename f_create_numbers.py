def create_numbers(number, extract: bool = False):
    if not extract:
        character_list = list(str(number))
        character_list.reverse()
        returned_list = []
        for character in range(len(character_list)):
            returned_list.append(character_list[character])
            if not (character + 1) % 3 and character:
                returned_list.append(",")
        returned_list.reverse()
        if returned_list[0] == ",":
            del returned_list[0]
        return "".join(returned_list)
    else:
        returned_number = number.split(",")
        try:
            return int("".join(returned_number))
        except ValueError:
            return None
