import uuid

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models

from apps.user.models import User
from apps.utils.models import GeoLocationModel, BaseModel


# Create your models here.
class Payment(BaseModel):
    PAYMENT_TYPE = [
        ('SINGLE', 'SINGLE'),
        ('MULTIPLE', 'MULTIPLE'),
    ]

    PAYMENT_STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    link_id = models.IntegerField(primary_key=True)
    link_url = models.CharField()
    title = models.CharField()
    type = models.CharField(choices=PAYMENT_TYPE)
    amount = models.IntegerField()
    redirect_url = models.CharField(blank=True)
    status = models.CharField(choices=PAYMENT_STATUS)
    expired_date = models.DateTimeField(null=True)
    created_from = models.CharField()
    is_address_required = models.BooleanField()
    is_phone_number_required = models.BooleanField()
    step = models.IntegerField()

    class Meta:
        unique_together = ['link_id', 'is_deleted']


class Disbursement(BaseModel):
    STATUS = ['PENDING', 'DONE', 'CANCELLED']

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    amount = models.IntegerField()
    status = models.CharField()
    timestamp = models.DateTimeField()
    bank_code = models.CharField()
    account_number = models.CharField()
    recipient_name = models.CharField()
    fee = models.IntegerField()
    beneficiary_email = models.TextField()
    idempotency_key = models.CharField()
    receipt = models.CharField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ['id', 'is_deleted']


class Event(GeoLocationModel):
    BANK_CODE = [('mandiri', 'mandiri'), ('bri', 'bri'), ('bni', 'bni'), ('bca', 'bca'), ('bsm', 'bsm'),
                 ('cimb', 'cimb'), ('muamalat', 'muamalat'), ('danamon', 'danamon'), ('permata', 'permata'),
                 ('bii', 'bii'), ('panin', 'panin'), ('uob', 'uob'), ('ocbc', 'ocbc'), ('citibank', 'citibank'),
                 ('artha', 'artha'), ('tokyo', 'tokyo'), ('dbs', 'dbs'), ('standard_chartered', 'standard_chartered'),
                 ('capital', 'capital'), ('anz', 'anz'), ('boc', 'boc'), ('bumi_arta', 'bumi_arta'), ('hsbc', 'hsbc'),
                 ('rabobank', 'rabobank'), ('mayapada', 'mayapada'), ('bjb', 'bjb'), ('dki', 'dki'),
                 ('daerah_istimewa', 'daerah_istimewa'), ('jawa_tengah', 'jawa_tengah'), ('jawa_timur', 'jawa_timur'),
                 ('jambi', 'jambi'), ('sumut', 'sumut'), ('sumatera_barat', 'sumatera_barat'),
                 ('riau_dan_kepri', 'riau_dan_kepri'), ('sumsel_dan_babel', 'sumsel_dan_babel'), ('lampung', 'lampung'),
                 ('kalimantan_selatan', 'kalimantan_selatan'), ('kalimantan_barat', 'kalimantan_barat'),
                 ('kalimantan_timur', 'kalimantan_timur'), ('kalimantan_tengah', 'kalimantan_tengah'),
                 ('sulselbar', 'sulselbar'), ('sulut', 'sulut'), ('nusa_tenggara_barat', 'nusa_tenggara_barat'),
                 ('bali', 'bali'), ('nusa_tenggara_timur', 'nusa_tenggara_timur'), ('maluku', 'maluku'),
                 ('papua', 'papua'), ('bengkulu', 'bengkulu'), ('sulawesi', 'sulawesi'),
                 ('sulawesi_tenggara', 'sulawesi_tenggara'), ('nusantara_parahyangan', 'nusantara_parahyangan'),
                 ('india', 'india'), ('mestika_dharma', 'mestika_dharma'), ('sinarmas', 'sinarmas'),
                 ('maspion', 'maspion'), ('ganesha', 'ganesha'), ('icbc', 'icbc'), ('qnb_kesawan', 'qnb_kesawan'),
                 ('btn', 'btn'), ('woori', 'woori'), ('tabungan_pensiunan_nasional', 'tabungan_pensiunan_nasional'),
                 ('bjb_syr', 'bjb_syr'), ('mega', 'mega'), ('bukopin', 'bukopin'), ('jasa_jakarta', 'jasa_jakarta'),
                 ('hana', 'hana'), ('mnc_internasional', 'mnc_internasional'), ('agroniaga', 'agroniaga'),
                 ('sbi_indonesia', 'sbi_indonesia'), ('royal', 'royal'), ('nationalnobu', 'nationalnobu'),
                 ('mega_syr', 'mega_syr'), ('ina_perdana', 'ina_perdana'), ('sahabat_sampoerna', 'sahabat_sampoerna'),
                 ('kesejahteraan_ekonomi', 'kesejahteraan_ekonomi'), ('bca_syr', 'bca_syr'), ('artos', 'artos'),
                 ('mayora', 'mayora'), ('index_selindo', 'index_selindo'),
                 ('victoria_internasional', 'victoria_internasional'), ('agris', 'agris'), ('chinatrust', 'chinatrust'),
                 ('commonwealth', 'commonwealth'), ('ccb', 'ccb'), ('danamon_syr', 'danamon_syr'),
                 ('victoria_syr', 'victoria_syr'), ('banten', 'banten'), ('mutiara', 'mutiara'),
                 ('panin_syr', 'panin_syr'), ('aceh', 'aceh'), ('btpn_syr', 'btpn_syr'), ('dinar', 'dinar'),
                 ('harda', 'harda'), ('e2pay', 'e2pay'), ('mas', 'mas'), ('prima', 'prima'),
                 ('yudha_bakti', 'yudha_bakti'), ('linkaja', 'linkaja'), ('dompetku', 'dompetku'),
                 ('shinhan', 'shinhan'), ('bukopin_syr', 'bukopin_syr'), ('cnb', 'cnb'), ('atmb_lsb', 'atmb_lsb'),
                 ('atmb_plus', 'atmb_plus'), ('antardaerah', 'antardaerah'), ('mantap', 'mantap'), ('eka', 'eka'),
                 ('finnet', 'finnet'), ('gopay', 'gopay'), ('ovo', 'ovo'), ('dana', 'dana'), ('shopeepay', 'shopeepay'),
                 ('sakuku', 'sakuku'), ('aladin', 'aladin'), ('dutamoney', 'dutamoney'), ('tokopedia', 'tokopedia'),
                 ('midtrans', 'midtrans'), ('permata_syr', 'permata_syr'), ('jawa_timur_syr', 'jawa_timur_syr'),
                 ('sinarmas_syr', 'sinarmas_syr'), ('jawa_tengah_syr', 'jawa_tengah_syr'), ('dki_syr', 'dki_syr'),
                 ('bii_syr', 'bii_syr'), ('ocbc_syr', 'ocbc_syr'), ('daerah_istimewa_syr', 'daerah_istimewa_syr'),
                 ('jambi_syr', 'jambi_syr'), ('sumut_syr', 'sumut_syr'), ('sumatera_barat_syr', 'sumatera_barat_syr'),
                 ('sumsel_dan_babel_syr', 'sumsel_dan_babel_syr'), ('kalimantan_selatan_syr', 'kalimantan_selatan_syr'),
                 ('kalimantan_barat_syr', 'kalimantan_barat_syr'), ('kalimantan_timur_syr', 'kalimantan_timur_syr'),
                 ('sulselbar_syr', 'sulselbar_syr'), ('artos_syr', 'artos_syr'), ('billfazz', 'billfazz'),
                 ('resona_perdania', 'resona_perdania'), ('america_na', 'america_na'),
                 ('jpmorgan_chase', 'jpmorgan_chase'), ('mizuho', 'mizuho'), ('bnp_paribas', 'bnp_paribas'),
                 ('amar', 'amar')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_host')
    account_number = models.CharField(null=True, blank=True, default=None)
    bank_code = models.CharField(null=True, choices=BANK_CODE, blank=True, default=None)
    name = models.CharField(max_length=100)
    description = models.TextField()
    preparation = models.TextField()
    image = CloudinaryField('image', null=True, blank=True, default=None)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    staffs = models.ManyToManyField(User, related_name='events_staff')
    supports = models.ManyToManyField(User, related_name='events_support')
    is_verified = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True, blank=True)
    disbursement = models.OneToOneField(Disbursement, on_delete=models.CASCADE, null=True, blank=True)
    total_donation = models.IntegerField(default=0)

    class Meta:
        unique_together = ['id', 'is_deleted']
        ordering = ['start_date']

    @property
    def image_url(self):
        return f'https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/{self.image}' if self.image else ''

    @property
    def payment_url(self):
        return self.payment.link_url if self.payment else ''

    @property
    def total_participant(self):
        return len(self.joined_users.all())

    def __str__(self):
        return self.name
