import praw
from dotenv import load_dotenv
import os

load_dotenv()


class RedditService:
    def __init__(self):
        self.__client_id = os.environ["REDDIT_CLIENT_ID"]
        self.__client_secret = os.environ["REDDIT_CLIENT_SECRET"]
        self.__username = os.environ["REDDIT_USERNAME"]
        self.__password = os.environ["REDDIT_PASSWORD"]
        self.reddit_client = praw.Reddit(
            user_agent=True,
            client_id=self.__client_id,
            client_secret=self.__client_secret,
            username=self.__username,
            password=self.__password,
        )

    def get_post_comments(self, url):
        if not self.reddit_client:
            return {}
        post = self.reddit_client.submission(url=url)
        res = []
        comments = post.comments
        comments.replace_more(limit=None)
        for comment in comments:
            res.append({"content": comment.body, "score": comment.score})
        return res
            

if __name__ == "__main__":
    redit_service = RedditService()
    url = "https://www.reddit.com/r/askSingapore/comments/158yje8/what_business_can_i_start_without_any_money/"
    url = "https://www.reddit.com/r/SaaS/comments/1gvbmin/dont_start_a_saas_if_you_want_to_make_money/"
    comments = redit_service.get_post_comments(url)
    for comment in comments:
        print(comment)
