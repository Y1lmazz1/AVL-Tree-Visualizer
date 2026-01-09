# 🌳 AVL Tree Visualizer & Practice Lab

Bu proje, AVL Ağacı veri yapısını hem görselleştiren hem de alıştırma yapma imkanı sunan modern bir Python uygulamasıdır.

## ✨ Özellikler
- **İki Farklı Mod:** - *Öğrenme Modu:* Her işlemi anında görselleştirir.
-**Alıştırma Modu:**Çözümü göstermeden önce kullanıcının tahmin etmesine olanak tanır.
- **Akıllı Tür Tanıma:** Ağaçta sadece sayı (int) veya sadece metin (string) kullanılmasını sağlar.
- **Gelişmiş Görselleştirme:** Graphviz motoru ile dengeli/dengesiz düğümleri renklendirir.
- **İşlem Günlüğü:** Yapılan tüm rotasyonları adım adım raporlar.
- **Rastgele Üretici:** 5-20 arası benzersiz sayı ile otomatik ağaç kurar.
- **Sıralama Seçenekleri:** In-order, Pre-order ve Post-order dizilimlerini canlı gösterir.

![Uygulama Ekran Görüntüsü]
  <img width="1918" height="997" alt="image" src="https://github.com/user-attachments/assets/7e3f7e82-a0bc-4f72-bd9f-aac3b249e57d" />


## 🛠️ Kurulum
1. Bilgisayarınıza [Graphviz](https://graphviz.org/download/) kurun ve `PATH` ayarlarını yapın.
2. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install Pillow graphviz
