from django.forms import ModelForm
from invest.models import *


class Form(ModelForm):
    class Meta:
        model = Stc001
        fields = ('stc_id', 'stc_name', 'stc_dvsn', 'now_price', 'face_price', 'tot_value', 'pgm_id')

