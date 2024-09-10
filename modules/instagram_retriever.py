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
          
        latest_posts = []
        latest_posts_count = 4 if ignore_pinned else 1
        for _ in range(latest_posts_count):
            post = next(posts_iterator)
            latest_posts.append(post)
        dates = [post.date for post in latest_posts]
        latest_date = max(dates)
    
        # 找到對應的貼文
        latest_post = latest_posts[dates.index(latest_date)] 
               
        content_urls = {}
        if latest_post.typename == 'GraphSidecar':
            for node in latest_post.get_sidecar_nodes():
                if node.is_video:
                    content_urls[node.video_url] = 'video'
                else:
                    content_urls[node.display_url] = 'image'
        else:
            # 單張圖片或單部影片
            if latest_post.is_video:
                content_urls[latest_post.url] = 'video'
                #content_urls[latest_post.video_url] = 'video'
            else:
                content_urls[latest_post.url] = 'image'                
        return {
            'caption': latest_post.caption,
            'hashtages': latest_post.caption_hashtags,
            'code': latest_post.shortcode,
            'content': content_urls         
        }

