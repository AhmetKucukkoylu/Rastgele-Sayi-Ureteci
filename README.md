# Collatz Kripto Projesi

Bu proje, Collatz sanısının (3n+1 problemi) kaotik dinamiklerinden yararlanan özgün bir blok şifreleme algoritması ve kriptografik olarak güvenli bir sözde rastgele sayı üreteci (PRNG) sunar.

## Proje Hakkında
Geleneksel AES (Advanced Encryption Standard) yapısından esinlenilen bu algoritma, Galois Alanları yerine Collatz dizilerinin tahmin edilemez doğasını kullanarak verileri şifreler. Eğitim ve araştırma amaçlı geliştirilmiştir.

## Algoritma Çalışma Mantığı

Algoritma üç temel bileşen üzerine kuruludur:

1.  **Collatz Anahtar Genişletme (Key Expansion)**:
    *   16 byte uzunluğundaki ana anahtar, `CollatzRNG` algoritması için bir tohum (seed) olarak kullanılır.
    *   Bu üreteç ile her şifreleme turu (round) için benzersiz alt anahtarlar (Round Keys) türetilir.

2.  **Dinamik S-Kutusu (Dynamic S-Box)**:
    *   Her şifreleme turunda, o tura ve anahtara özel dinamik bir S-Kutusu (Substitution Box) oluşturulur.
    *   S-Kutusu, Fisher-Yates karıştırma algoritması ve Collatz dizileri kullanılarak 0-255 arası değerlerin rastgele permütasyonuyla elde edilir.

3.  **Tur İşlemleri (Round Functions)**:
    *   **SubBytes (Bayt Değiştirme)**: Veri bloğundaki her bayt, dinamik S-Kutusu kullanılarak değiştirilir. Bu işlem "karışıklık" (confusion) sağlar.
    *   **ShiftRows (Satır Kaydırma)**: Veri matrisinin satırları belirli oranlarda kaydırılır. Bu işlem "yayılım" (diffusion) sağlar.
    *   **AddRoundKey (Anahtar Ekleme)**: Veri bloğu, o turun anahtarı ile XOR işlemine sokulur.

### Akış Diyagramı

Algoritmanın genel işleyiş şeması aşağıdadır:

```mermaid
graph TD
    Basla[Girdi: Düz Metin ve Anahtar] --> AnahtarGen[Anahtar Genişletme (CollatzRNG)]
    AnahtarGen --> Dongu{Tur Döngüsü (1..9)}
    Dongu -->|Her Tur| SBoxUret[Dinamik S-Kutusu Üret]
    SBoxUret --> Karistir[SubBytes (Karıştırma)]
    Karistir --> Kaydir[ShiftRows (Kaydırma)]
    Kaydir --> AnahtarEkle[AddRoundKey (Anahtar XOR)]
    AnahtarEkle --> Dongu
    Dongu -->|Döngü Sonu| Final[Final Turu]
    Final --> Cikti[Çıktı: Şifreli Metin]
```

### Sözde Kod (Pseudo-Code)

Şifreleme fonksiyonunun basitleştirilmiş mantığı:

```text
FONKSİYON Sifrele(DuzMetin, Anahtar):
    // 1. Hazırlık
    Durum = DuzMetin
    TurAnahtarlari = AnahtarGenislet(Anahtar)

    // 2. Başlangıç Turu
    AnahtarEkle(Durum, TurAnahtarlari[0])

    // 3. Ana Turlar (9 Tur)
    DÖNGÜ i = 1'den 9'a:
        SBox = SBoxUret(TurAnahtarlari[i], i)
        BaytDegistir(Durum, SBox)
        SatirKaydir(Durum)
        AnahtarEkle(Durum, TurAnahtarlari[i])

    // 4. Final Turu
    SBox = SBoxUret(TurAnahtarlari[10], 10)
    BaytDegistir(Durum, SBox)
    SatirKaydir(Durum)
    AnahtarEkle(Durum, TurAnahtarlari[10])

    DÖNDÜR Durum (SifreliMetin)
```

## Proje Dosya Yapısı

- **`src/`**: Kaynak kod dizini.
    - `cipher.py`: `CollatzBlockCipher` sınıfı (Şifreleme motoru).
    - `prng.py`: `CollatzRNG` sınıfı (Rastgele sayı üreteci).
    - `collatz_core.py`: Collatz matematik fonksiyonları.
- **`tests/`**: Birim testleri.
- **`demo.py`**: Örnek kullanım ve test betiği.

## Kurulum ve Çalıştırma

Proje Python 3 üzerinde çalışır. Kodu test etmek için ana dizindeki demo betiğini çalıştırabilirsiniz:

```bash
python3 demo.py
```

### Beklenen Çıktı

```text
=== Collatz Crypto Demo ===
Key: b'SecretKey_123456'
Cipher initialized with Collatz Key Expansion.

Plaintext: b'Attack at Dawn!!'
Ciphertext (hex): ...
Decrypted: b'Attack at Dawn!!'

SUCCESS: Decryption matched original plaintext.
```
