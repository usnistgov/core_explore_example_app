from django.conf import settings

if not settings.configured:
    settings.configure()


RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
