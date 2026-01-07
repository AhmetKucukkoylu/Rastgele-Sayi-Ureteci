# Collatz Kripto Projesi (Rastgele Sayı Üreteci)

Bu proje, **Collatz Sanısı**'nın (3n+1 Problemi) kaotik ve tahmin edilemez doğasından yararlanan yenilikçi bir **Blok Şifreleme Algoritması** ve **Sözde Rastgele Sayı Üreteci (PRNG)** sunar.

## 📌 Proje Hakkında

Geleneksel şifreleme yöntemleri (örneğin AES), karmaşık matematiksel yapılar (Galois Alanları) kullanırken; bu proje, matematiğin çözülememiş en büyük problemlerinden biri olan Collatz dizilerinin kaosunu bir güvenlik katmanı olarak kullanır. Amaç, hem güvenli bir şifreleme sunmak hem de kriptografik rastgelelik için alternatif bir yöntem geliştirmektir.

---

## ⚙️ Algoritma Nasıl Çalışır?

Sistemin güvenliği üç temel saç ayağına dayanır:

### 1. Collatz Anahtar Genişletme (Key Expansion)
Kullanıcının girdiği 16 byte'lık (128-bit) anahtar doğrudan kullanılmaz. Bunun yerine:
*   Anahtar, `CollatzRNG` modülüne bir "tohum" (seed) olarak verilir.
*   Collatz dizileri (bir sayı çift ise 2'ye böl, tek ise 3n+1 yap) kullanılarak, her şifreleme turu (round) için birbirinden tamamen farklı **Tur Anahtarları** üretilir.

### 2. Dinamik S-Kutusu (Dynamic S-Box)
AES gibi algoritmalar sabit bir değişim kutusu (S-Box) kullanır. Bu algoritma ise:
*   Her turda ve her anahtar için **özgün** bir S-Kutusu oluşturur.
*   Bu kutu, 0'dan 255'e kadar olan sayıların Collatz kaosu ile karıştırılması (Fisher-Yates Shuffle) sonucu elde edilir.
*   Bu sayede, saldırganın sistemi analiz etmesi imkansız hale gelir çünkü S-Kutusu sürekli değişmektedir.

### 3. Tur İşlemleri (Round Functions)
Veri, 10 tur boyunca şu işlemlerden geçirilir:
*   **SubBytes (Karıştırma)**: Her veri baytı, o anki Dinamik S-Kutusu kullanılarak değiştirilir.
*   **ShiftRows (Yayılım)**: Veri satırları kaydırılarak bitlerin yerleri değiştirilir.
*   **AddRoundKey (Gizleme)**: Veri, o turun anahtarı ile XOR işlemine sokulur.

---

## 📊 Akış Diyagramı (Flowchart)

Algoritmanın çalışma prensibi aşağıdaki şemada gösterilmiştir:

```mermaid
graph TD
    Basla[BAŞLA: Düz Metin ve Anahtar] --> Ayarlar[Hazırlık: Anahtarı Al ve Durumu Başlat]
    Ayarlar --> AnahtarGen[Anahtar Genişletme (CollatzRNG)]
    
    AnahtarGen --> TurDongusu{Tur Döngüsü (1..9)}
    
    TurDongusu -->|Her Tur İçin| SBoxUret[Dinamik S-Kutusu Oluştur]
    SBoxUret --> BaytDegistir[SubBytes: Baytları Karıştır]
    BaytDegistir --> SatirKaydir[ShiftRows: Satırları Kaydır]
    SatirKaydir --> AnahtarEkle[AddRoundKey: Tur Anahtarını Ekle]
    
    AnahtarEkle --> TurDongusu
    
    TurDongusu -->|Döngü Bitti| FinalTuru[Final Turu (10. Tur)]
    FinalTuru --> SBoxFinal[S-Kutusu Oluştur]
    SBoxFinal --> BaytFinal[SubBytes]
    BaytFinal --> SatirFinal[ShiftRows]
    SatirFinal --> AnahtarFinal[AddRoundKey]
    
    AnahtarFinal --> Bitis[BİTİŞ: Şifreli Metin]
    
    style Basla fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Bitis fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TurDongusu fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
```

---

## 📝 Sözde Kod (Pseudo-Code)

Aşağıda, şifreleme fonksiyonunun adım adım nasıl çalıştığını gösteren sözde kod bulunmaktadır:

```text
FONKSİYON Sifrele(DuzMetin, Ana Anahtar):

    // 1. ADIM: HAZIRLIK
    Durum Matrisi = DuzMetin
    Tur Anahtarlari = CollatzAnahtarGenislet(Ana Anahtar)

    // 2. ADIM: BAŞLANGIÇ TURU
    AnahtarEkle(Durum Matrisi, Tur Anahtarlari[0])

    // 3. ADIM: ANA TURLAR (1'den 9'a kadar tekrarla)
    DÖNGÜ Tur Sayisi = 1'den 9'a:
        
        // a. O tura özel S-Kutusu üret
        S_Kutusu = CollatzSBoxUret(Tur Anahtarlari[Tur Sayisi])
        
        // b. Baytları karıştır (Confusion)
        BaytDegistir(Durum Matrisi, S_Kutusu)
        
        // c. Satırları kaydır (Diffusion)
        SatirKaydir(Durum Matrisi)
        
        // d. Tur anahtarını ekle
        AnahtarEkle(Durum Matrisi, Tur Anahtarlari[Tur Sayisi])

    // 4. ADIM: FİNAL TURU
    S_Kutusu = CollatzSBoxUret(Tur Anahtarlari[10])
    BaytDegistir(Durum Matrisi, S_Kutusu)
    SatirKaydir(Durum Matrisi)
    AnahtarEkle(Durum Matrisi, Tur Anahtarlari[10])

    // SONUÇ
    DÖNDÜR Durum Matrisi (Şifrelenmiş Metin)
```

---

## 📂 Proje Dosyaları

*   `src/`: Kaynak kodların bulunduğu klasör.
    *   `cipher.py`: Şifreleme algoritmasının kendisi.
    *   `prng.py`: Rastgele sayı üreteci.
    *   `collatz_core.py`: Matematiksel çekirdek dosyası.
*   `demo.py`: Hızlı başlangıç ve test dosyası.

## 🚀 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki komutu terminale yazmanız yeterlidir:

```bash
python3 demo.py
```

### Beklenen Ekran Çıktısı

```text
=== Collatz Crypto Demo ===
Key: b'SecretKey_123456'
Cipher initialized with Collatz Key Expansion.

Plaintext: b'Attack at Dawn!!'
Ciphertext (hex): 4b0f9a0739d8...
Decrypted: b'Attack at Dawn!!'

SUCCESS: Decryption matched original plaintext.
```
