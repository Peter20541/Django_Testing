from django.apps import AppConfig


class BlogPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_page'
    def ready(self):
        import blog_page.signals
