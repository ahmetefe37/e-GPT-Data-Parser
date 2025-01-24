# Circuit Data Converter for AI Training

Bu proje, elektronik devre şemalarını ve çıktılarını AI model eğitimi için uygun formata dönüştüren bir araçtır. Devre şemaları (.asc) ve çıktıları (.plt) JSON ve CSV formatlarına dönüştürülür ve Alpaca veri formatına uygun hale getirilir.

## 🚀 Özellikler

- Devre şemalarını ve çıktılarını otomatik eşleştirme
- Devre açıklamalarını instruction dosyalarından okuma
- JSON ve CSV formatlarına dönüştürme
- Otomatik yedekleme sistemi (5 aşamalı)
- Excel uyumlu CSV çıktısı

## 📁 Proje Yapısı

```
ai-model/
├── circuit-files/
│   ├── instructions/    # Devre açıklama dosyaları (.txt)
│   ├── outputs/         # Devre çıktı dosyaları (.plt)
│   └── schematics/     # Devre şema dosyaları (.asc)
├── json-files/
│   ├── stage1/         # Güncel JSON dosyaları
│   ├── stage2/         # 1. yedek
│   ├── stage3/         # 2. yedek
│   ├── stage4/         # 3. yedek
│   └── stage5/         # 4. yedek
├── csv-files/
│   ├── stage1/         # Güncel CSV dosyaları
│   ├── stage2/         # 1. yedek
│   ├── stage3/         # 2. yedek
│   ├── stage4/         # 3. yedek
│   └── stage5/         # 4. yedek
├── app.py              # Ana uygulama
├── json_converter.py   # JSON dönüştürme modülü
├── json_updater.py     # JSON güncelleme aracı
├── csv_converter.py    # CSV dönüştürme modülü
└── csv_updater.py      # CSV güncelleme aracı
```

## 🛠️ Kurulum

1. Projeyi klonlayın:
```bash
git clone [repo-url]
cd ai-model
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 💻 Kullanım

### Tüm İşlemleri Çalıştırma
Ana uygulamayı çalıştırarak tüm dönüşüm işlemlerini gerçekleştirin:
```bash
python app.py
```

### Ayrı Ayrı Çalıştırma
1. Sadece JSON güncellemesi için:
```bash
python json_updater.py
```

2. Sadece CSV dönüşümü için:
```bash
python csv_updater.py
```

## 📄 Veri Formatı

### JSON Format
```json
{
    "instruction": "[devre açıklaması]",
    "input": "[devre şeması]",
    "response": "[devre çıktısı]"
}
```

### CSV Format
Her satır şu sütunları içerir:
- `instruction`: Devre açıklaması
- `input`: Devre şeması
- `response`: Devre çıktısı

## 🔄 Yedekleme Sistemi

- Her güncelleme işleminde mevcut veriler bir üst stage'e taşınır
- stage1: En güncel veriler
- stage2-stage5: Yedek veriler
- stage5'teki veriler silinip yerlerine yeni yedek gelir

## 🧪 Test

1. Test devresi eklemek için:
   - Devre şemasını `circuit-files/schematics/` klasörüne
   - Devre çıktısını `circuit-files/outputs/` klasörüne
   - Devre açıklamasını `circuit-files/instructions/` klasörüne ekleyin
2. `app.py`'yi çalıştırın
3. `json-files/stage1/` ve `csv-files/stage1/` klasörlerinde dönüştürülmüş dosyaları kontrol edin

## 📝 Notlar

- CSV dosyaları UTF-8-SIG encoding ile oluşturulur
- Excel'de CSV dosyalarını açarken "Veri -> Metinden/CSV'den" seçeneğini kullanın
- Dosya isimleri uzantılar hariç eşleşmelidir (örn: `test_circuit.asc` ve `test_circuit.plt`)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📜 Lisans

Bu proje [MIT](LICENSE) lisansı altında lisanslanmıştır.
