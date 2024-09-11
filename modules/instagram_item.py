import instaloader

class PostItem():
    def __init__(self, type, url, video_url=None):
        self.type = type
        self.url = url
        self.video_url = video_url

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
          
        #最後latest_posts_count個貼文
        latest_posts = []
        latest_posts_count = 4 if ignore_pinned else 1
        for _ in range(latest_posts_count):
            post = next(posts_iterator)
            latest_posts.append(post)
        dates = [post.date for post in latest_posts]
        latest_date = max(dates)
    
        # 最後一個貼文
        latest_post = latest_posts[dates.index(latest_date)] 
         
        # 製作PostItem      
        post_items = []
        if latest_post.typename == 'GraphSidecar':
            for node in latest_post.get_sidecar_nodes():
                if node.is_video:
                    post_items.append(
                        PostItem('video', node.url, node.video_url))
                else:
                    post_items.append(
                        PostItem('image', node.display_url))
        else:
            # 單張圖片或單部影片
            if latest_post.is_video:
                post_items.append(
                    PostItem('video', latest_post.url, latest_post.video_url))
            else:
                post_items.append(
                    PostItem('image', latest_post.url))
        return {
            'caption': latest_post.caption,
            'hashtages': latest_post.caption_hashtags,
            'code': latest_post.shortcode,
            'post_items': post_items         
        }

