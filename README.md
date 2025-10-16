# Renk-Sembolizmi
Gemini API ve RAG (Retrieval Augmented Generation) mimarisi kullanılarak oluşturulmuş, renklerin sembolik anlamları ve insan üzerindeki etkileri hakkında bilgi veren bir sohbet robotu.
### 📌 PROJENİN AMACI
Bu projenin temel amacı, RAG (Retrieval Augmented Generation) temelli bir chatbot geliştirerek, bir web arayüzü üzerinden sunmaktır.

### 🧪 ÇÖZÜM MİMARİSİ VE KULLANILAN TEKNOLOJİLER 
* **Mimari:** Retrieval Augmented Generation (RAG) mimarisi.
* **Büyük Dil Modeli:** Gemini API.
* **Veri İşleme:** LangChain (Özel Prompt ve k=10 ile optimize edilmiştir).
* **Vektör Veritabanı:** ChromaDB.
* **Web Arayüzü:** Streamlit.

### 📊 VERİ SETİ HAKKINDA BİLGİ 
* Veri seti, renklerin psikolojik etkilerini, sembolik anlamlarını ve kurumsal/mimari kullanım alanlarını içeren "Renklerin Sembolik Anlamları ve Etkileri" başlıklı bir PDF dokümanıdır.

### 📄 ÇALIŞMA KILAVUZU VE ELDE EDİLEN SONUÇLAR 
* Proje gereksinimleri `requirements.txt` dosyasındadır.
* Uygulama, **`app.py`** dosyası ile Streamlit üzerinde çalışır ve genel karşılaştırmalı sorulara doğru yanıt verecek şekilde optimize edilmiştir.

### 🌐 WEB ARAYÜZÜ (DEPLOY) LİNKİ 
Projenin çalışan web uygulamasına aşağıdaki linkten erişilebilir:
https://renk-sembolizmi-eh5necjsybz8vkuliqmvt4.streamlit.app/

### 🖼️ ÜRÜN KILAVUZU / ÇALIŞMA KANITI

Aşağıdaki ekran görüntüsü, chatbot'un veri setindeki bilgileri başarıyla çekip karşılaştırmalı cevap üretebildiğini göstermektedir:

![Çalışan Chatbot Ekran Görüntüsü] <img width="977" height="750" alt="chatbot_calisiyor" src="https://github.com/user-attachments/assets/99fe3fa3-5cbe-4b56-a8bd-e157918bdc23" />

