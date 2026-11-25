"""Oturum 1'den sonraki görevin kontrolü.

Kullanım: make odev-kontrol N=01
Betik bronze tablolarını kaynak dosyalarla karşılaştırır, karar kaydının bölümlerini sınar ve
bütün adımlar TAMAM olduğunda altı haneli kanıt kodunu yazar. Kod, görev teslimiyle birlikte platforma yüklenir.
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

LAB_KOK = Path(os.environ.get("LAB_KOK", Path(__file__).resolve().parents[2]))
DURUM = LAB_KOK / ".lab"
TOPLU = ["toplu_ulasim_2024_01.csv.gz", "toplu_ulasim_2024_02.csv.gz"]
TRAFIK = ["trafik_2024_01.csv.gz"]
BOLUMLER = ["Bağlam", "Karar", "Gerekçe", "Sonuçlar"]


def baglanti():
    import duckdb
    b = duckdb.connect()
    b.execute((DURUM / "baglan.sql").read_text(encoding="utf-8"))
    return b


def kaynak_satir(b, dosya):
    return b.execute(f"SELECT count(*) FROM read_csv('{LAB_KOK / 'veri' / dosya}')").fetchall()[0][0]


def tablo_sina(b, tablo, dosyalar, asgari_snapshot):
    var = b.execute("SELECT count(*) FROM duckdb_tables() WHERE database_name = 'lake' AND schema_name = 'bronze' "
                    "AND table_name = ?", [tablo]).fetchall()[0][0]
    if not var:
        return False, f"lake.bronze.{tablo} bulunamadı", 0
    kolonlar = {k[0] for k in b.execute(f"SELECT * FROM lake.bronze.{tablo} LIMIT 0").description}
    eksik = {"_kaynak_dosya", "_yukleme_zamani"} - kolonlar
    if eksik:
        return False, f"bronze kararındaki kolonlar eksik: {', '.join(sorted(eksik))}", 0
    snapshot = b.execute(f"SELECT count(*) FROM iceberg_snapshots('lake.bronze.{tablo}')").fetchall()[0][0]
    if snapshot < asgari_snapshot:
        return False, f"{snapshot} snapshot var, en az {asgari_snapshot} bekleniyor", 0
    toplam = 0
    for dosya in dosyalar:
        tabloda = b.execute(f"SELECT count(*) FROM lake.bronze.{tablo} WHERE _kaynak_dosya = ?", [dosya]).fetchall()[0][0]
        kaynakta = kaynak_satir(b, dosya)
        if tabloda != kaynakta:
            return False, f"{dosya}: tabloda {tabloda} satır, kaynakta {kaynakta} satır", 0
        toplam += tabloda
    return True, f"{len(dosyalar)} dosya, {toplam} satır, {snapshot} snapshot", toplam


def karar_kaydi():
    yol = LAB_KOK / "docs" / "kararlar" / "0001-mimari.md"
    if not yol.exists():
        return False, "docs/kararlar/0001-mimari.md bulunamadı"
    metin = yol.read_text(encoding="utf-8")
    if not re.search(r"^Durum:\s*\S", metin, re.M):
        return False, "Durum satırı eksik"
    bos = []
    for bolum in BOLUMLER:
        eslesme = re.search(rf"^##\s*{bolum}\s*$(.*?)(?=^##\s|\Z)", metin, re.M | re.S)
        icerik = [s for s in (eslesme.group(1).splitlines() if eslesme else []) if s.strip() and not s.strip().startswith("<!--")]
        if not icerik:
            bos.append(bolum)
    if bos:
        return False, f"boş ya da eksik bölüm: {', '.join(bos)}"
    return True, "dört bölüm dolu"


def main():
    print("Oturum 1 görevi sınanıyor.\n")
    b = baglanti()
    sonuclar = []
    tamam1, ayrinti1, toplu = tablo_sina(b, "toplu_ulasim", TOPLU, 2)
    sonuclar.append(("Toplu ulaşım bronze tablosu", tamam1, ayrinti1))
    tamam2, ayrinti2, trafik = tablo_sina(b, "trafik", TRAFIK, 1)
    sonuclar.append(("Trafik bronze tablosu", tamam2, ayrinti2))
    tamam3, ayrinti3 = karar_kaydi()
    sonuclar.append(("Mimari karar kaydı", tamam3, ayrinti3))
    genislik = max(len(a) for a, _, _ in sonuclar)
    for ad, tamam, ayrinti in sonuclar:
        print(f"  {ad:<{genislik}}  {'TAMAM' if tamam else 'HATA ':5}  {ayrinti}")
    print()
    if all(t for _, t, _ in sonuclar):
        kullanici = os.environ.get("GITHUB_USER") or subprocess.run(["git", "config", "user.name"], capture_output=True,
                                                                    text=True).stdout.strip() or "bilinmiyor"
        kod = hashlib.sha256(f"odev-01|{kullanici}|{toplu}|{trafik}".encode()).hexdigest()[:6].upper()
        print(f"Görev tamam. Kanıt kodu: {kod} (GitHub kullanıcısı: {kullanici})")
        sys.exit(0)
    print("Görev tamamlanmadı. HATA satırlarındaki açıklama eksik adımı gösterir.")
    sys.exit(1)


if __name__ == "__main__":
    main()
