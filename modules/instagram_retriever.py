import instaloader

class InstagramItem():
    def __init__(self, username):
        ig_loader = instaloader.Instaloader()
        self.profile = instaloader.Profile.from_username(ig_loader.context, username)
    
    def get_user_profile(self):
        return {
            'username': self.profile.username,
            'fullname': self.profile.full_name,
            'biography': self.profile.biography
        }
    
    def get_latest_posts(self, ignore_pinned=True):
        posts_iterator = self.profile.get_posts()
        latest_post = next(posts_iterator)
        if ignore_pinned:
            while (latest_post.is_pinned):
                latest_post = next(posts_iterator)
        return {
            'caption': latest_post.caption,
            'hashtages': latest_post.caption_hashtags
        }

