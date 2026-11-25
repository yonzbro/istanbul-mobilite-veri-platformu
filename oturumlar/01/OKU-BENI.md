# Oturum 1 | Çalışma dosyası

Bu dosya Oturum 1'in üç uygulamasını tarif eder. Her blok kısa bir soruyla başlar, ardından konu anlatılır ve uygulama gelir. Uygulamanın çözümü bloğun sonunda birlikte yapılır.

`make sql` komutu DuckDB'yi lab kataloğuna bağlı olarak açar ve bütün sorgular bu oturumda çalışır. Bir SQL dosyası DuckDB içinde `.read` komutuyla çalışır; örnek: `.read oturumlar/01/u1_1_ham_veri_kesfi.sql`. `make sql` ve `.read` ayrı ayrı yazılır: `.read` satırı DuckDB'nin `calisma D` istemi göründükten sonra yazılır.

## U1.1 Tekrar gönderilen gün (15 dakika)

- Görev: Ocak 2024 toplu ulaşım dosyasında kaynağın iki kez gönderdiği günü buluyor ve o günün iki kez geldiğini gösteriyorsunuz.
- `ham_ocak` tablosu anlatımda başlangıç dosyasıyla oluştu. Tablo yoksa DuckDB'de `.read oturumlar/01/u1_1_ham_veri_kesfi.sql` komutu tabloyu kurar.
- Her günün satır sayısını ve toplam yolculuğunu veren sorgunun iskeleti aşağıdadır. `GROUP BY` ve `ORDER BY` satırlarını siz tamamlıyorsunuz; sıralama tekrar gönderilen günü listenin en üstüne getirir:

```
SELECT transition_date,
       count(*) AS satir,
       sum(number_of_passage) AS yolculuk
FROM ham_ocak
GROUP BY ...
ORDER BY ...;
```

- Bulduğunuz günü bir hafta önceki aynı günle karşılaştırıyorsunuz. Bunun için `WHERE` koşuluyla ikinci bir sorgu yazıyorsunuz; tarih `DATE '2024-01-15'` biçiminde yazılır.
- Sorgular DuckDB'ye doğrudan yazılır ve noktalı virgülle biter. Ekrana sığmayan kolonlar `…` ile gizlenir; `.last` son sonucu bütün kolonlarıyla açar, q tuşu DuckDB'ye döner.
- Günü ve iki satır sayısını Zoom sohbetine yazıyorsunuz.
- Erken bitirenler `town` ve `number_of_passenger` kolonlarında kaç satırın boş olduğunu ve `line_name` kolonunda bozuk karakter taşıyan hat adlarını buluyor. Boş değeri `IS NULL` koşulu bulur.

## U1.2 Bronze tablosu (20 dakika)

- Görev: Ocak ve Şubat 2024 dosyalarını `lake.bronze.toplu_ulasim` adlı bir Iceberg tablosuna yüklüyorsunuz.
- Başlangıç kodu `oturumlar/01/u1_2_bronze.sql` dosyasındadır. Partition dönüşümünü `PARTITIONED BY` satırına yazıyor, dosyayı kaydediyor ve DuckDB'de `.read oturumlar/01/u1_2_bronze.sql` ile çalıştırıyorsunuz. Seçenekler: `month(transition_date)`, `day(transition_date)` ve `transport_type_id`.
- Şubat dosyasını (`veri/toplu_ulasim_2024_02.csv.gz`) aynı tabloya `INSERT INTO lake.bronze.toplu_ulasim` ile ekliyorsunuz. `SELECT` kısmı Ocak'takiyle aynıdır, yalnızca dosya adı değişir. `INSERT INTO` kolonları sırayla eşler; `SELECT` listesinin sırası korunur.
- Tablodaki satırları `_kaynak_dosya` kolonuna göre sayıyor ve `iceberg_snapshots('lake.bronze.toplu_ulasim')` ile snapshot sayısına bakıyorsunuz. Her kaynak dosyanın satır sayısı tabloda aynen yer alır ve tabloda iki snapshot bulunur.
- Partition seçiminizi, toplam satır sayısını ve snapshot sayısını Zoom sohbetine yazıyorsunuz.
- Şubat dosyası tabloya bir kez yüklenir. İki kez yüklendiyse tablo `DROP TABLE lake.bronze.toplu_ulasim;` ile silinir ve iki yükleme yeniden yapılır.
- Erken bitirenler ilk snapshot'taki satır sayısını `AT (VERSION => ...)` ifadesiyle buluyor; snapshot kimliği `iceberg_snapshots` çıktısında yer alır.

## U1.3 Mimari karar kaydı (15 dakika)

- Görev: Projenin ilk mimari karar kaydını `docs/kararlar/0001-mimari.md` dosyasında yazıyorsunuz.
- Kayıt batch ve streaming bileşenlerini, gecikme hedefini, tablo formatını ve kataloğu belirler.
- Kayıtta Durum satırı ve dolu dört bölüm (Bağlam, Karar, Gerekçe, Sonuçlar) bulunur. Karar bölümü tek cümledir; Gerekçe en az bir ölçülebilir ihtiyaca dayanır.
- Kararın tek cümlelik özetini Zoom sohbetine yazıyorsunuz.
- Erken bitirenler elediği bir seçeneği ve elenme gerekçesini Gerekçe bölümüne "Elenen seçenekler:" satırıyla ekliyor.

## Oturumlar arası görev (30-45 dakika, Oturum 2'ye kadar)

- Trafik yoğunluğu verisinin Ocak 2024 dosyası (`veri/trafik_2024_01.csv.gz`) `lake.bronze.trafik` tablosuna yüklenir. Tablo bronze kararına uyar: kaynağı değiştirmez, `_kaynak_dosya` ve `_yukleme_zamani` kolonlarını taşır.
- `lake.bronze.toplu_ulasim` tablosunda Ocak ve Şubat dosyaları yer alır.
- Karar kaydı dört bölümüyle tamamlanır.
- Kontrol komutu `make odev-kontrol N=01` olur. Bütün adımlar TAMAM olduğunda betik kanıt kodunu yazar; kod ve depo bağlantısı Tech İstanbul platformundaki göreve yüklenir.

## Ortam çalışmazsa

Uygulamalar eğitmen ekranından takip edilir ve aynı görevler oturumdan sonra tamamlanır.
