import tweepy
from bots.streamlistenerbase import StreamListenerBase


class LikeRetweetBot(StreamListenerBase):
    def __init__(self, api, logger):
        super().__init__(api, logger)
        self.json_file = "autoretweet/users.json"

    def on_status(self, status):
        if status.user.id_str in self.tracking:
            status.favorite()
            status.retweet()
            self.logger.info("Re-tweeted and liked tweet from {}: {}".format(status.user.id_str, status.text))

    def run_bot(self):
        while True:
            stream = tweepy.Stream(self, self.api.auth)
            stream.filter(track=self.users, languages=["en"])
            self.logger.info("Searching tweets")

    def start(self):
        pass
