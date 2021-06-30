from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
    	import user.signals


# class UserConfig(AppConfig):
#     name = 'user'
#     def ready(self):
#     	import user.signals