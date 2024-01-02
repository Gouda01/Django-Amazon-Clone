from .models import Settings
from django.core.cache import cache

def get_settings(request):
    
    #Check data in cash
    try :
        settings_data = cache.get('settings_data')
    except Exception:
        settings_data = Settings.objects.last()
        cache.set('settings_data',settings_data,60*60*24)

    return {'settings_data' : settings_data}