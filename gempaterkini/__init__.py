from bs4 import BeautifulSoup
import requests

def ekstraksi_data():
    """
    Tanggal: 5 Januari 2022
    Waktu: 03:34:28 WIB
    Magnitudo: 4.7
    Kedalaman: 12 km
    Lokasi: LS=7.01 LS  BT= 105.28 BT
    Pusat Gempa: Pusat gempa berada di laut 50 km Barat Daya Sumur
    Dirasakan: Dirasakan (Skala MMI): II Pandeglang, II Jiput, II Muncul
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        title = soup.find('title')
        tanggalwaktu = soup.find('span', {'class': 'waktu'})
        tanggalwaktu = tanggalwaktu.text.split(',');
        tanggal = tanggalwaktu[0]
        waktu = tanggalwaktu[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        i = 0
        magnitudo = None
        ls = None
        bt = None
        pusat = None
        kedalaman = None
        dirasakan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1
    
    hasil = dict()
    hasil['title'] = title.text
    hasil['tanggal'] = tanggal #'5 Januari 2022'
    hasil['waktu']  = waktu #'03:34:28 WIB'
    hasil['magnitudo']  = magnitudo # 4.7
    hasil['kedalaman']  = kedalaman #'12 km'
    hasil['koordinat'] = {'ls': ls, 'bt': bt}
    hasil['lokasi']  = lokasi
    hasil['dirasakan']  = dirasakan #'Dirasakan (Skala MMI): II Pandeglang, II Jiput, II Muncul'

    return hasil


def tampilkan_data(result):
    if result is None:
        print("Tidak bisa menemukan data terkini")
        return None

    print(result['title'])
    print(f"Tanggal {result['tanggal']}")
    print(f"Waktu {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi: {result['lokasi']}")
    print(f"Dirasakan {result['dirasakan']}")

if __name__ == "__main__":
    result = ekstraksi_data()
    tampilkan_data(result)