from django.db import models


# 주식기본
class Stc001(models.Model):
    stc_id = models.CharField(max_length=45)
    stc_name = models.CharField(max_length=45)
    stc_dvsn = models.CharField(max_length=45)
    now_price = models.BigIntegerField(default=0)
    face_price = models.BigIntegerField(default=0)
    tot_value = models.BigIntegerField(default=0)
    pgm_id = models.CharField(max_length=10)
    cdate = models.DateTimeField(auto_now_add=True)


# 주식일별내역
class Stc002(models.Model):
    base_dt = models.CharField(max_length=45)
    stc_id = models.CharField(max_length=45)
    mod_cls_price = models.BigIntegerField(default=0)
    cls_price = models.BigIntegerField(default=0)
    diff_price = models.BigIntegerField(default=0)
    strt_price = models.BigIntegerField(default=0)
    high_price = models.BigIntegerField(default=0)
    low_price = models.BigIntegerField(default=0)
    deal_qnt = models.BigIntegerField(default=0)
    pgm_id = models.CharField(max_length=10)
    cdate = models.DateTimeField(auto_now_add=True)
