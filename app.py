import streamlit as st
from openai import OpenAI

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Akıllı CV Asistanı", page_icon="🤖")

# --- SENİN BİLGİLERİN (Botun Hafızası) ---
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


# --- ANA EKRAN ---
st.title("🤖 [Adın]'ın Yapay Zeka Asistanı")
st.write("Merhaba! Ben [Adın]'ın dijital ikiziyim. CV'mi analiz ettim.")
st.write("Bana projelerim, yeteneklerim veya hedeflerim hakkında dilediğinizi sorabilirsiniz.")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Size nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- YAPAY ZEKA MANTIĞI ---
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    # 1. Kullanıcı mesajını ekrana yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. ANAHTARI GİZLİ KASADAN AL (Otomatik)
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        st.error("HATA: API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından 'Secrets' kısmını kontrol edin.")
        st.stop()

    # 3. OpenAI'ya Bağlan
    try:
        client = OpenAI(api_key=api_key)
        
        system_instruction = f"""
        Sen şu kişinin profesyonel asistanısın:
        {RESUME_DATA}
        
        Sadece bu bilgilere dayanarak cevap ver.
        Samimi ve profesyonel ol.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages
        )
        
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")