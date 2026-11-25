-- Oturum 1 | U1.1 Ham veri keşfi
-- make sql ile açılan DuckDB oturumunda çalışır: .read oturumlar/01/u1_1_ham_veri_kesfi.sql
CREATE OR REPLACE TABLE ham_ocak AS
SELECT * FROM read_csv('veri/toplu_ulasim_2024_01.csv.gz');

DESCRIBE ham_ocak;
SELECT count(*) AS satir FROM ham_ocak;
SELECT * FROM ham_ocak LIMIT 10;

-- Ekrana sığmayan kolonlar için: .last (sağ ok tuşuyla kaydırılır, q ile çıkılır)
-- Uygulamanın sorguları DuckDB'ye doğrudan yazılır. Bu dosyayı yeniden
-- çalıştırmak tabloyu baştan kurar.
