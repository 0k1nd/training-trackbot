from rest_framework.throttling import SimpleRateThrottle


class BotRateThrottle(SimpleRateThrottle):
    scope = "bot"

    def get_cache_key(self, request, view):
        return "bot-global"
