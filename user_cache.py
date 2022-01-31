
class UserCache:
    """
    Stores user IDs that have been retrieved from the Twitter API
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def find_user(self, screen_name):
        try:
            with open(self.file_name, 'r') as cache_file:
                for line in cache_file:
                    parts = line.split(':')
                    if parts[0] == screen_name:
                        return parts[1].strip()
        except FileNotFoundError:
            open(self.file_name, 'w').close()
        return None

    def write_user(self, screen_name, user_id):
        with open(self.file_name, 'a') as cache_file:
            cache_file.write(f'{screen_name}: {user_id}\n')
