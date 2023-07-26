# Generated by Django 4.2.2 on 2023-07-26 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0013_event_account_number_event_bank_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='account_number',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='bank_code',
            field=models.CharField(blank=True, choices=[('mandiri', 'mandiri'), ('bri', 'bri'), ('bni', 'bni'), ('bca', 'bca'), ('bsm', 'bsm'), ('cimb', 'cimb'), ('muamalat', 'muamalat'), ('danamon', 'danamon'), ('permata', 'permata'), ('bii', 'bii'), ('panin', 'panin'), ('uob', 'uob'), ('ocbc', 'ocbc'), ('citibank', 'citibank'), ('artha', 'artha'), ('tokyo', 'tokyo'), ('dbs', 'dbs'), ('standard_chartered', 'standard_chartered'), ('capital', 'capital'), ('anz', 'anz'), ('boc', 'boc'), ('bumi_arta', 'bumi_arta'), ('hsbc', 'hsbc'), ('rabobank', 'rabobank'), ('mayapada', 'mayapada'), ('bjb', 'bjb'), ('dki', 'dki'), ('daerah_istimewa', 'daerah_istimewa'), ('jawa_tengah', 'jawa_tengah'), ('jawa_timur', 'jawa_timur'), ('jambi', 'jambi'), ('sumut', 'sumut'), ('sumatera_barat', 'sumatera_barat'), ('riau_dan_kepri', 'riau_dan_kepri'), ('sumsel_dan_babel', 'sumsel_dan_babel'), ('lampung', 'lampung'), ('kalimantan_selatan', 'kalimantan_selatan'), ('kalimantan_barat', 'kalimantan_barat'), ('kalimantan_timur', 'kalimantan_timur'), ('kalimantan_tengah', 'kalimantan_tengah'), ('sulselbar', 'sulselbar'), ('sulut', 'sulut'), ('nusa_tenggara_barat', 'nusa_tenggara_barat'), ('bali', 'bali'), ('nusa_tenggara_timur', 'nusa_tenggara_timur'), ('maluku', 'maluku'), ('papua', 'papua'), ('bengkulu', 'bengkulu'), ('sulawesi', 'sulawesi'), ('sulawesi_tenggara', 'sulawesi_tenggara'), ('nusantara_parahyangan', 'nusantara_parahyangan'), ('india', 'india'), ('mestika_dharma', 'mestika_dharma'), ('sinarmas', 'sinarmas'), ('maspion', 'maspion'), ('ganesha', 'ganesha'), ('icbc', 'icbc'), ('qnb_kesawan', 'qnb_kesawan'), ('btn', 'btn'), ('woori', 'woori'), ('tabungan_pensiunan_nasional', 'tabungan_pensiunan_nasional'), ('bjb_syr', 'bjb_syr'), ('mega', 'mega'), ('bukopin', 'bukopin'), ('jasa_jakarta', 'jasa_jakarta'), ('hana', 'hana'), ('mnc_internasional', 'mnc_internasional'), ('agroniaga', 'agroniaga'), ('sbi_indonesia', 'sbi_indonesia'), ('royal', 'royal'), ('nationalnobu', 'nationalnobu'), ('mega_syr', 'mega_syr'), ('ina_perdana', 'ina_perdana'), ('sahabat_sampoerna', 'sahabat_sampoerna'), ('kesejahteraan_ekonomi', 'kesejahteraan_ekonomi'), ('bca_syr', 'bca_syr'), ('artos', 'artos'), ('mayora', 'mayora'), ('index_selindo', 'index_selindo'), ('victoria_internasional', 'victoria_internasional'), ('agris', 'agris'), ('chinatrust', 'chinatrust'), ('commonwealth', 'commonwealth'), ('ccb', 'ccb'), ('danamon_syr', 'danamon_syr'), ('victoria_syr', 'victoria_syr'), ('banten', 'banten'), ('mutiara', 'mutiara'), ('panin_syr', 'panin_syr'), ('aceh', 'aceh'), ('btpn_syr', 'btpn_syr'), ('dinar', 'dinar'), ('harda', 'harda'), ('e2pay', 'e2pay'), ('mas', 'mas'), ('prima', 'prima'), ('yudha_bakti', 'yudha_bakti'), ('linkaja', 'linkaja'), ('dompetku', 'dompetku'), ('shinhan', 'shinhan'), ('bukopin_syr', 'bukopin_syr'), ('cnb', 'cnb'), ('atmb_lsb', 'atmb_lsb'), ('atmb_plus', 'atmb_plus'), ('antardaerah', 'antardaerah'), ('mantap', 'mantap'), ('eka', 'eka'), ('finnet', 'finnet'), ('gopay', 'gopay'), ('ovo', 'ovo'), ('dana', 'dana'), ('shopeepay', 'shopeepay'), ('sakuku', 'sakuku'), ('aladin', 'aladin'), ('dutamoney', 'dutamoney'), ('tokopedia', 'tokopedia'), ('midtrans', 'midtrans'), ('permata_syr', 'permata_syr'), ('jawa_timur_syr', 'jawa_timur_syr'), ('sinarmas_syr', 'sinarmas_syr'), ('jawa_tengah_syr', 'jawa_tengah_syr'), ('dki_syr', 'dki_syr'), ('bii_syr', 'bii_syr'), ('ocbc_syr', 'ocbc_syr'), ('daerah_istimewa_syr', 'daerah_istimewa_syr'), ('jambi_syr', 'jambi_syr'), ('sumut_syr', 'sumut_syr'), ('sumatera_barat_syr', 'sumatera_barat_syr'), ('sumsel_dan_babel_syr', 'sumsel_dan_babel_syr'), ('kalimantan_selatan_syr', 'kalimantan_selatan_syr'), ('kalimantan_barat_syr', 'kalimantan_barat_syr'), ('kalimantan_timur_syr', 'kalimantan_timur_syr'), ('sulselbar_syr', 'sulselbar_syr'), ('artos_syr', 'artos_syr'), ('billfazz', 'billfazz'), ('resona_perdania', 'resona_perdania'), ('america_na', 'america_na'), ('jpmorgan_chase', 'jpmorgan_chase'), ('mizuho', 'mizuho'), ('bnp_paribas', 'bnp_paribas'), ('amar', 'amar')], null=True),
        ),
    ]
