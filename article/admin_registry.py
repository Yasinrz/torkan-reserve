from notifications.admin_site import custom_admin_site
from .admin import *

custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Tag ,TagAdmin)
custom_admin_site.register(Article ,ArticleAdmin)
custom_admin_site.register(ArticleLike,ArticleLikeAdmin)
custom_admin_site.register(Comment,CommentAdmin)
custom_admin_site.register(Gallery,GalleryAdmin)