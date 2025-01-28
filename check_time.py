from datetime import datetime

def is_valide_date(date_string,date_format="%Y-%m-%d-%H-%M"):
        if datetime.strptime(date_string,date_format):
            return True
        else:
              return False