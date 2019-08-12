from AideCan.views import *
from django.urls import path,include




urlpatterns = [
  path('',first_page,name='first_page'),
  path('activate/<str:uidb64>/<str:token>/<int:id>', activate, name='activate'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('<int:id>/profile', profile_view, name='profile'),
  path('<int:id>/ajouter_mammographie', add_mammography, name='add_mammography'),
  path('<int:id>/label_mammography/<int:id_mammo>', label_one, name='label_one'),
  path('<int:id>/show_label/<int:id_label>', show_label, name='show_label'),
  path('<int:id>/show_all_labels', show_all_labels, name='show_all_labels'),
  path('<int:id>/random_labeling', random_labling, name='random_labling'),
  path('<int:id>/supM/<int:id_mammo>', sup_mammography, name='sup_mammography'),
  path('<int:id>/supD/<int:id_diag>', sup_diagnostic, name='sup_diagnostic'),
  path('<int:id>/statistic', statistic, name='statistic'),

  path('a/', random_labling , name='a'),
  path('b/', tel, name='tel'),

]
