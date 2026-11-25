-- Oturum 1 | U1.2 Bronze katmanı
-- Partition kararınız PARTITIONED BY ifadesine yazıldıktan sonra make sql oturumunda çalışır.
CREATE TABLE lake.bronze.toplu_ulasim
PARTITIONED BY (month(transition_date)) AS
SELECT * EXCLUDE (filename),
       parse_filename(filename) AS _kaynak_dosya,
       now() AS _yukleme_zamani
FROM read_csv('veri/toplu_ulasim_2024_01.csv.gz', filename = true);

SELECT * FROM iceberg_snapshots('lake.bronze.toplu_ulasim');
