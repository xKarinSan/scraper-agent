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
        self.__hard_limit = 100

    def get_post_comments(self, url):
        if not self.reddit_client:
            return []

        res = []
        post = self.reddit_client.submission(url=url)
        comments = post.comments
        comments.replace_more(limit=None)
        for comment in comments:
            res.append({"content": comment.body, "score": comment.score})
        return res

    def get_relevant_posts(
        self, subreddits, sort_by="relevance", limit=25, search_query=""
    ):
        # try:
        print("subreddits",subreddits)
        print("sort_by",sort_by)
        print("limit",limit)
        print("search_query",search_query)
        if not subreddits:
            return []

        res = []
        subreddits = "+".join(subreddits)
        if limit >= self.__hard_limit:
            limit = self.__hard_limit
            
        subreddit_obj = self.reddit_client.subreddit(subreddits)
        if search_query:
            submissions = subreddit_obj.search(query=search_query, sort=sort_by, limit=limit)
        else:
            if sort_by == "hot":
                submissions = subreddit_obj.hot(limit=limit)
            elif sort_by == "new":
                submissions = subreddit_obj.new(limit=limit)
            elif sort_by == "top":
                submissions = subreddit_obj.top(limit=limit)
            elif sort_by == "rising":
                submissions = subreddit_obj.rising(limit=limit)
            else:
                submissions = subreddit_obj.hot(limit=limit)
        print("submissions",submissions)

        for submission in submissions:
            # print("submission:",submission)
            res.append(
                {
                    "title": submission.title,
                    "contents": submission.selftext,
                    "comment_count": submission.num_comments,
                    "submission_score": submission.score,
                }
            )
        print(len(res))
        return res
        # except:
        #     return []


if __name__ == "__main__":
    reddit_service = RedditService()
    url = "https://www.reddit.com/r/askSingapore/comments/158yje8/what_business_can_i_start_without_any_money/"
    url = "https://www.reddit.com/r/SaaS/comments/1gvbmin/dont_start_a_saas_if_you_want_to_make_money/"
    # comments = reddit_service.get_post_comments(url)
    # for comment in comments:
    #     print(comment)

    submissions = reddit_service.get_relevant_posts(["SaaS"], "latest", 5)
    # for submission in submissions:
    #     print(submission)
