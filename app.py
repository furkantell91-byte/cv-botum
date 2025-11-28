import streamlit as st
from openai import OpenAI

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Akıllı CV Asistanı", page_icon="🤖")

# --- SENİN CV BİLGİLERİN (Botun Hafızası) ---
# Buraya kendi bilgilerini detaylıca yaz. Bot burayı okuyup öğrenecek.
RESUME_DATA = """
İsim: [Furkan TELLİ]
Rol: iş arayan bir kişi aynı zamada yazılım öğreniyor
Lokasyon: Eskişehir, Türkiye

Özet:
Merhaba! Ben [Furkan TELLİ], iş arayan aynı zamanda yazılım öğrenen ve diğer alanlarda da kendini geliştiren bir kişyim.

Teknik Beceriler:
- Programlama: Python (başlangıç seviyesi), microsoft office programları, Sap(orta seviye) 
- Araçlar: VS Code, Streamlit, Git
- Dil: Türkçe (Anadil), İngilizce (orta seviye)

Projeler:
Senaryo ve kitap yazarlığı alanında çeşitli projelerim var.

Eğitim:
- [Anadolu Üniversitesi Açıköğretim Fakültesi] - [Halkla İlişkiler ve Reklamcılık]

Hedefler:
- Halkla ilişkiler,reklamcılık veya pazarlama alanlarında kendimi geliştirebileceğim bir iş bulmak
- yazılım ve yapay zeka alanlarında kendimi geliştirmek
- 1 yıl içinde ingilizceyi ileri seviyeye taşımak

İletişim:
- E-posta: Furkantell91@gmail.com
- telefon: +90 542 253 66 18

Çalıştığı iş yerleri ve Aldığım Görevler:
1- Eti Sarp LOJİSTİK
- Ofis personeli ve Lojistik personeli olarak çalıştım.

Sertifikalar:
- Bilgisayar İşletmenliği (M.E.B)
- İş Sağlığı ve Güvenliği (M.E.B)

Kendinini Tanıtır mısın?
- 25 yaşındayım, Eskişehir'de yaşıyorum.Bir yandan halkla ilişkiler,reklamcılık ve pazarlam alanlarında kendimi geliştiryorum, bir yandan da yeni teknolojilerle ilgileniyorum
4.5 yıl lojistik sektöründe çalıştım. Ardından askerlik vazifesi için işten ayrıldım.Yeterli bilgi ve birikimim
olmasına rağmen lojistik sektöründen ziyade kendi alanım olan ve yapmaktan zevk alabileceğim, iyi ikili ilişkiler
kurup kendimi geliştirebileceğim, kendime ve çalıştığım kuruma doğru değerleri katabileceğim bir iş arıyorum.
Pazarlama sektöründe profesyonel olarak çalışmasam da beş yıldan fazla kendi ticari işlerimi yürüttüğüm için
aslında her zaman işin içindeydim. Teorik olarak da bilgilerimin yeterli olduğunu düşünüyorum ve kendimi
geliştirmeye devam ediyorum.Halkla ilişkiler ve reklamcılık alanlı da yine okulunu okuduğum ve teorik olarak
bilgimin yeterli olduğu bir alandır. Bu alanlarda çalışmamın bana ve çalıştığım işletmeye fazlasıyla deüğer
katacağını düşünüyorum.

Güçlü yönlerin nelerdir?
- Hayatta birçok zorlukla baş etmek zorunda kalıyoruz. Ben de bu durumları fazlasıyla deneyimlemiş bir kişiyim.
Çalıştırken okumak zorunda kaldım.Ve bir üniversitede örgün bir eğitim alamadım. Bunun bende bir eksiklik olduğunu düşündüğüm 
için her zaman daha fazla araştırdım ve öğrenme hevesimi hiç kaybetmedim.En güçlü yönümün araştırma ve öğrenme isteğim 
olduğunu düşünüyorum.

Neden sizi işe almalıyız?
- Durmadan kendimi geliştirme çabasında olan bir insanım. Benim için iyi diye bir iey yoktur.Her zaman iyinin
daha iyisi, daha hızlısı ve daha akıllıcası vardır.Öğrenmek konusunda aç gözlüyümdür.Öğrendiğim şeylerle yetinmek
ve stabil çalışma hayatı benim için yeterli değildir. Bir şeyi öğrenirken kendime bir fayda sağlayacağını 
düşünerek değil, budan zevk aldığım için üstüne düşerim.

"""

# --- YAN MENÜ (ANAHTAR GİRİŞİ) ---
with st.sidebar:
    st.header("🔑 Ayarlar")
    st.info("Botun zekasını çalıştırmak için OpenAI API Anahtarı gerekir.")
    # Kullanıcı anahtarını buraya girecek
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="sk-... ile başlayan kod")
    st.markdown("[Anahtar Almak İçin Tıkla](https://platform.openai.com/api-keys)")
    st.divider()
    st.caption("Not: Anahtarınız kaydedilmez, sadece bu oturumda kullanılır.")

# --- ANA EKRAN ---
st.title("🤖 [Furkan]'ın Yapay Zeka Asistanı")
st.write("Merhaba! Ben sıradan bir bot değilim. [Furkanın]'ın CV'sini analiz ettim.")
st.write("Bana dilediğiniz soruyu sorabilirsiniz. *(Örn: 'Neden işe almalıyız', 'Güçlü yönleri neler')*")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Hakkımda ne merak ediyorsunuz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- YAPAY ZEKA MANTIĞI ---
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    # 1. Kullanıcı mesajını ekrana yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Anahtar kontrolü
    if not openai_api_key:
        st.warning("⚠️ Lütfen cevap alabilmek için sol menüye OpenAI API Anahtarınızı giriniz.")
        st.stop()

    # 3. OpenAI'ya Bağlan
    try:
        client = OpenAI(api_key=openai_api_key)
        
        # Botun kişiliğini ve bilgisini tanımlıyoruz (System Prompt)
        system_instruction = f"""
        Sen şu kişinin profesyonel yapay zeka asistanısın:
        {RESUME_DATA}
        
        GÖREVLERİN:
        1. Sadece yukarıdaki CV bilgilerine dayanarak cevap ver.
        2. Cevapların samimi, profesyonel ve kısa olsun.
        3. İşverenlere karşı bu adayı en iyi şekilde temsil et.
        4. Bilmediğin bir şey sorulursa dürüstçe "Bilgim yok" de.
        """

        # Yapay zekadan cevap iste
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages
        )
        
        msg = response.choices[0].message.content
        
        # Cevabı ekrana yaz
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        st.info("Eğer 'Quota' veya 'RateLimit' hatası alıyorsanız, OpenAI hesabınızda kredi bitmiş olabilir.")