import subprocess
import re
# Çıktıyı kaydetmek için önce çıktıyı yakalamak istediğimizi belirtiyoruz.
komut_ciktisi = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode('latin-1')

# Listelenen tüm wifi adlarını çekmek için.
profil_isimleri = re.findall("All User Profile     : (.*)\\r", komut_ciktisi)

# Tüm wifi kullanıcı adlarını ve şifreleri için liste oluşturuyoruz.
wifi_listesi = []

if len(profil_isimleri) != 0:
    for isim in profil_isimleri:
        # Her wifi bağlantısını, wifi_listesi değişkenine ekliyoruz.
        wifi_profili = {}
        # Güvenlik anahtarı mevcut değilse, şifreyi alıyoruz.
        profil_bilgisi = subprocess.run(["netsh", "wlan", "show", "profile", isim], capture_output=True).stdout.decode('latin-1')

        if re.search("Security key           : Absent", profil_bilgisi):
            continue
        else:
            # Wifilerin ssid'sini atayın.
            wifi_profili["ssid"] = isim
            # Şifre için "key=clear" komutunu çalıştırın.
            profil_bilgisi_sifre = subprocess.run(["netsh", "wlan", "show", "profile", isim, "key=clear"], capture_output=True).stdout.decode('latin-1')

            sifre = re.search("Key Content            : (.*)\\r", profil_bilgisi_sifre)

            # Bazı wifi bağlantılarında şifre olmayabilir.
            if sifre is None:
                wifi_profili["sifre"] = None
            else:
                # Şifresi olan grubu, sözlüğe atıyoruz.
                wifi_profili["sifre"] = sifre[1]
            # Wifi bilgilerini wifi_listesi değişkenine ekliyoruz.
            wifi_listesi.append(wifi_profili)

for wifi in wifi_listesi:
    print(wifi)
