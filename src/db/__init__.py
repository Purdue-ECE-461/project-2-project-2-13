import logging


# memory-only database
DB = {
    'package': {
    }
}

def get(table, key=None):
    if table in DB:
        if key == None:
            return DB[table]
        elif key in DB[table]:
            return DB[table][key]
        else:
            logging.error('Unable to find key `{key}` in table `{table}`')
    else:
        logging.error('Unable to find table `{table}`')

    return None


def set(table, key, value):
    if table in DB:
        DB[table][key] = value
    else:
        logging.error('Unable to find table `{table}`')

def reset(table):
    if table in DB:
        DB[table] = {}
    else:
        logging.error('Unable to find table `{table}`')