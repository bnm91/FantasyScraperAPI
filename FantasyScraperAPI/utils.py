# transforms list of rows of csv strings into a single "cvs file" string that is presentable on the web
def csv_list_to_csv_string(csv_list):
    csv_string = ''
    for row in csv_list:
        csv_string += row
        csv_string += ' <br />'
    return csv_string


def find_between_r(s, first):
    try:
        start = s.rindex(first) + len(first)
        end = s.find(u'\xa0')
        return s[start:end]
    except ValueError:
        return ""



# breaks dictionary describing a League Scoreboard row into a csv row
def comma_separate_values(row_dict):
    row_string = ''

    for key in row_dict.keys():
        row_string += str(row_dict[key]) + ','
        
    return row_string



def create_csv_from_list(rowdict_list, header_row):
    csv_list = []
    csv_list.append(comma_separate_values(header_row))

    for rowdict in rowdict_list:
        csv_list.append(comma_separate_values(rowdict))
    
    return csv_list_to_csv_string(csv_list)

