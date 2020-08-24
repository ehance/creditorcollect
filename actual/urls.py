from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
import hello.views
import products.urls
import blog.urls
import banks.urls
import tradier.urls
from . import views


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^tradier-account-opened/$', views.TradierAccountOpenedPage.as_view(), name='tradier-account-opened'),
    url(r'^fiduciary/$', views.FiduciaryPage.as_view(), name='fiduciary'),
    url(r'^team/$', views.TeamPage.as_view(), name='team'),
    url(r'^pricing/$', views.PricingPage.as_view(), name='pricing'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(accounts.urls, namespace='accounts')),
    url(r'^products/', include(products.urls, namespace='products')),
    url(r'^blog/', include(blog.urls, namespace='blog')),
    url(r'^accounts/', include(banks.urls, namespace='banks')),
    url(r'^about/', include('contact_form.urls')),
    #url(r'^plan/$', views.TeamPage.as_view(), name='team'),

    url(r'^plan/$', views.plan, name='plan'),
    url(r'^plan/assets$', views.assets, name='assets'),
    url(r'^plan/spending$', views.spending, name='spending'),
    url(r'^plan/estate$', views.estate, name='estate'),
    url(r'^plan/utility$', views.utility, name='utility'),
    url(r'^plan/liquidity$', views.liquidity, name='liquidity'),
    url(r'^plan/actions$', views.actions, name='actions'),
    url(r'^plan/chart/(?P<name>\w*)', views.chart, name='chart'),

    url(r'^test/user_info/$', views.test_user_info, name='test_user_info'),

    url(r'^plan/investing/investing$', views.investing, name='investing'),
    # url(r'^plan/faq$', views.faq, name='faq'),
    url(r'^plan/faq/(?P<name>\w*)', views.faq, name='faq'),
    url(r'^tradier/', include(tradier.urls, namespace='tradier')),

   # url(r'^$', hello.views.index, name='index'),
   #url(r'^db', hello.views.db, name='db'),
   # url(r'^admin/', include(admin.site.urls)),
]
# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)