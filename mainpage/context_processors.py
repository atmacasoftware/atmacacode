from adminpage.models import SiteSettings


def site_settings(request):
    site = SiteSettings.objects.all().last()
    return dict(site_settings=site)