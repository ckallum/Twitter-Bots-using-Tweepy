import simplejson as json
import tweepy


class StreamListenerBase(tweepy.StreamListener):
    def __init__(self, api, logger):
        super().__init__()
        self.users = []
        self.tracking = []
        self.me = api.me()
        self.api = api
        self.logger = logger
        self.json_file = ""

    def on_connect(self):
        if not self.tracking:
            raise Exception("No users being tracked")
        else:
            self.logger.info("Bot connected, tracking {}".format([user["handle"] for user in self.tracking]))

    def on_status(self, status):
        pass

    def add_users(self):
        handles = input("Enter the handles of the users")
        if not handles:
            self.logger.info("No handles entered")
            self.add_users()
        else:
            handles = list(handles.strip(" "))
            for handle in handles:
                user_id = self.api.lookup_users(screen_names=handle)
                self.tracking.append(user_id)
                self.users.append({"id": user_id, "handle": handle})

    def remove_users(self):
        handles = input("Enter the handles of the users")
        if not handles:
            self.logger.info("No handles entered")
            self.remove_users()
        else:
            handles = list(handles.strip(" "))
            for handle in handles:
                if handle not in handles:
                    self.logger.info("Invalid handle entered: {}, continuing..".format(handle))
                    pass
                user_id = self.api.lookup_users(screen_names=handle)
                self.tracking.remove(user_id)
                self.users.remove({"id": user_id, "handle": handle})

    def update_json(self):
        with open(self.json_file, "w") as file:
            json.dump(file, self.users)

    def import_jsons(self):
        with open(self.json_file, "r") as file:
            self.users = json.load(file)
            self.tracking = [user["id"] for user in self.users]

    def choose(self):
        with open("messages/option_messages/choice.txt", "r") as option:
            choice = input(option.read())
        if choice == 1:
            self.add_users()
            self.logger.info("Users added, bot now running")
            self.run_bot()
        elif choice == 2:
            self.remove_users()
            self.logger.info("Users added, bot now running")
            self.run_bot()
        else:
            self.run_bot()

    def run_bot(self):
        pass

    def start(self):
        self.import_jsons()
        self.choose()
        self.update_json()
