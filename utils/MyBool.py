class MyBool(object):
    def str_to_bool(my_bool: str):
        if my_bool.lower() == 'true':
            return True
        elif my_bool.lower() == 'false':
            return False

