# 0001 Mimari: batch, streaming ve tablo formatı

Durum: Önerildi
Tarih: 23 Kasım 2026

## Bağlam

Platform iki ayrı istek karşılayacak. Aylık hat raporu, ay kapandıktan sonra hat
ve ilçe bazında yolcu toplamlarını ister. Durak yoğunluğu ise 5 dakikadan eski
olmayan geçiş sayılarını ve eşik alarmını ister. Kaynaklar aylık CSV dosyaları
ve geçiş olaylarıdır. Veriyi DuckDB ve Spark birlikte kullanacaktır.

## Karar

Aylık dosyalar batch olarak bronze, silver ve gold katmanlarından geçer; geçiş
olayları Kafka ve Structured Streaming ile aynı kataloğa yazılır; tablo formatı
Iceberg, katalog Apache Polaris olur.

## Gerekçe

- Aylık rapor bir gün gecikmeyi kabul eder, bu yüzden batch yeterlidir.
- Durak yoğunluğu en geç 5 dakikada güncellenmelidir, bu yüzden akış gerekir.
- Akış işi gün boyu çalışır, batch iş günde birkaç dakika sürer; sürekli
  çalışan bileşen yalnızca ihtiyaç duyan istek için kullanılır.
- Bronze tablosunu DuckDB yazdı, Spark aynı kataloğdan okudu; Iceberg ve Polaris
  birden çok motorun aynı tabloyu kopyalamadan kullanmasını sağlar.
- Elenen seçenek: bütün verinin Kafka ve akış motoruyla işlenmesi. Aylık rapor
  bir gün gecikmeyi kabul ettiği için gün boyu çalışan akış işinin maliyeti
  gerekçesizdir.

## Sonuçlar

- İki yol işletilecek: batch için zamanlama (Airflow), akış için sürekli izleme.
- Bronze, kaynağı olduğu gibi saklar; tekrar gönderilen 10 Ocak günü ve bozuk
  karakterli hat adları silinmez, temizlik silver'da yapılır.
- Her bronze satırında `_kaynak_dosya` ve `_yukleme_zamani` bulunur, bu yüzden
  yüklemenin izi sürülebilir.
- Kişisel veri maskeleme ve erişim rolleri sonraki oturumlara bırakıldı.