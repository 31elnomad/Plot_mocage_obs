

def __convert_data__(file_unit, unit, data):
    if unit != '1':
        if unit == 'DU':
            if file_unit == 'molec m-2':
                data = data / 2.6867e20
        else:
            raise Exception ("Convert {} n'est pas implémenté")
    else:
        unit = file_unit
    return date, unit
