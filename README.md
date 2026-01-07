# Collatz Crypto

Bu proje, Collatz sanısının (3n+1 problemi) kaotik dinamiklerine dayalı özgün bir blok şifreleme algoritması ve sözde rastgele sayı üreteci (PRNG) uygular.

## Algoritma Nasıl Çalışır?

Bu şifreleme algoritması, AES (Advanced Encryption Standard) yapısından esinlenmiştir ancak AES'in matematiksel temelleri (Galois Fields) yerine Collatz dizilerinin karmaşık ve tahmin edilemez yapısını kullanır.

### Temel Bileşenler:

1.  **Collatz Anahtar Genişletme (Key Expansion)**:
    *   16 byte'lık ana anahtar, bir `CollatzRNG` (Rastgele Sayı Üreteci) tohumu olarak kullanılır.
    *   Collatz dizileri kullanılarak her tur için benzersiz "Tur Anahtarları" (Round Keys) üretilir.

2.  **Dinamik S-Kutusu (Dynamic S-Box)**:
    *   AES'te sabit olan S-Kutusu, burada her tur ve her anahtar için *dinamik* olarak oluşturulur.
    *   Bu, Collatz tabanlı bir karıştırma işlemi ile 0-255 arası sayıların yerlerinin değiştirilmesiyle (Fisher-Yates shuffle) yapılır.

3.  **Tur İşlemleri (Round Functions)**:
    *   **SubBytes**: Her byte, o tur için üretilen S-Kutusu kullanılarak değiştirilir (Confusion - Karışıklık).
    *   **ShiftRows**: Satırlar döngüsel olarak kaydırılır (Diffusion - Yayılım).
    *   **AddRoundKey**: Blok, o turun anahtarı ile XOR işlemine tabi tutulur.

## Pseudo-Code (Sözde Kod) Şeması

Aşağıda şifreleme işleminin basitleştirilmiş mantığı bulunmaktadır:

```text
FONKSİYON Encrypt(Plaintext, Key):
    // 1. Hazırlık
    State = Plaintext
    RoundKeys = ExpandKey(Key)  // CollatzRNG kullanarak anahtarları üret

    // 2. Başlangıç Turu
    AddRoundKey(State, RoundKeys[0])

    // 3. Ana Turlar (1'den 9'a kadar)
    DÖNGÜ i = 1 TO 9:
        SBox = GenerateSBox(RoundKeys[i], i) // Collatz ile o tura özel S-Box yap
        SubBytes(State, SBox)                // Byte'ları karıştır
        ShiftRows(State)                     // Satırları kaydır
        AddRoundKey(State, RoundKeys[i])     // Anahtarı ekle

    // 4. Final Turu (MixColumns yok)
    SBox = GenerateSBox(RoundKeys[10], 10)
    SubBytes(State, SBox)
    ShiftRows(State)
    AddRoundKey(State, RoundKeys[10])

    DÖNDÜR State (Ciphertext)
```

### Akış Diyagramı

Algoritmanın genel işleyişi aşağıdaki gibidir:

```mermaid
graph TD
    A[Girdi: Metin ve Anahtar] --> B[Anahtar Genişletme (CollatzRNG)]
    B --> C{Tur Döngüsü (1..9)}
    C -->|Her Tur İçin| D[Dinamik S-Kutusu Üret]
    D --> E[SubBytes (Karıştırma)]
    E --> F[ShiftRows (Kaydırma)]
    F --> G[AddRoundKey (Anahtar Ekleme)]
    G --> C
    C -->|Döngü Bitti| H[Final Turu]
    H --> I[Çıktı: Şifreli Metin]
```

## Proje Yapısı

- `src/`: Kaynak kodları içerir.
    - `cipher.py`: `CollatzBlockCipher` sınıfı (Şifreleme mantığı).
    - `prng.py`: `CollatzRNG` sınıfı (Rastgele sayı üretimi).
    - `collatz_core.py`: Temel Collatz fonksiyonları.
- `tests/`: Test dosyaları.
- `demo.py`: Örnek çalıştırma betiği.

## Nasıl Çalıştırılır

Projeyi çalıştırmak ve demoyu görmek için terminal'de şu komutu çalıştırın:

```bash
python3 demo.py
```

### Örnek Çıktı

```text
=== Collatz Crypto Demo ===
Key: b'SecretKey_123456'
Cipher initialized with Collatz Key Expansion.

Plaintext: b'Attack at Dawn!!'
Ciphertext (hex): ...
Decrypted: b'Attack at Dawn!!'

SUCCESS: Decryption matched original plaintext.
```
