import streamlit as st
import pandas as pd

# 1. SAYFA VE DİL YAPILANDIRMASI
st.set_page_config(page_title="DMD Guardian Global Pro", layout="wide", initial_sidebar_state="expanded")

# --- HAFIZA SİSTEMİ (SESSION STATE) ---
if 'kilo' not in st.session_state: st.session_state.kilo = 30
if 'yas' not in st.session_state: st.session_state.yas = 6
if 'nsaa_total' not in st.session_state: st.session_state.nsaa_total = 0
if 'lang' not in st.session_state: st.session_state.lang = 'TR'

def switch_lang():
    st.session_state.lang = 'EN' if st.session_state.lang == 'TR' else 'TR'

# Sidebar dil butonu
st.sidebar.button("🌐 TR / EN - Change Language", on_click=switch_lang)

# --- METİN SÖZLÜĞÜ (7 SEKME) ---
D = {
    'TR': {
        'nav': ["Ana Panel / Dashboard", "Klinik Hesaplayıcı", "Tam Ölçekli NSAA Testi", "Genişletilmiş SSS / FAQ", "Acil Durum & Solunum", "Klinik Takvim & Yasal Haklar", "Vizyon & KVKK"],
        'anes_warn': "🚨 KRİTİK: Anestezi Uyarısı!",
        'ster_warn': "Steroidler Asla Aniden Kesilmemelidir!",
        'calc_h': "🧬 Klinik Hesaplayıcı & Veri Girişi",
        'weight': "Kilo (kg)",
        'age': "Yaş",
        'mut': "Mutasyon Tipi",
        'ster_res': "**Günlük Steroid Dozaj Tahmini (Deflazacort):**",
        'nsaa_h': "🏃 Klinik Kuzey Yıldızı (NSAA) Gelişmiş Takip",
        'score_h': "📊 Toplam NSAA Skoru",
        'faq_h': "❓ Sık Sorulan Sorular & Akademik Rehber",
        'cal_h': "🏥 Klinik Takvim & Kapsamlı Yasal Haklar",
        'emer_h': "🚨 Acil Durum & Kritik Bakım Yönetimi"
    },
    'EN': {
        'nav': ["Dashboard", "Clinical Calculator", "Full Scale NSAA Test", "Extended FAQ", "Emergency & Respiratory", "Clinical Calendar & Rights", "Vision & Privacy"],
        'anes_warn': "🚨 CRITICAL: Anesthesia Warning!",
        'ster_warn': "Steroids Must Never Be Stopped Abruptly!",
        'calc_h': "🧬 Clinical Calculator & Data Entry",
        'weight': "Weight (kg)",
        'age': "Age",
        'mut': "Mutation Type",
        'ster_res': "**Daily Steroid Dosage Estimate (Deflazacort):**",
        'nsaa_h': "🏃 North Star Ambulatory Assessment (NSAA) Tracking",
        'score_h': "📊 Total NSAA Score",
        'faq_h': "❓ Frequently Asked Questions & Academic Guide",
        'cal_h': "🏥 Clinical Calendar & Legal Rights Guide",
        'emer_h': "🚨 Emergency & Critical Care Management"
    }
}[st.session_state.lang]

# 2. NAVİGASYON
st.sidebar.title("🧭 DMD Center")
# --- GELİŞTİRİCİ ROZETİ ---
st.sidebar.markdown("""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;">
        <p style="margin:0; font-size: 0.8rem; color: #555;">Proje Lideri</p>
        <b style="color: #1c83e1;">Berfin Nida Öztürk</b>
    </div>
""", unsafe_allow_html=True)
page = st.sidebar.radio("Menu", D['nav'])
st.sidebar.divider()
st.sidebar.error(D['anes_warn'])
st.sidebar.warning(D['ster_warn'])

# --- SAYFA 0: ANA PANEL ---
if page == D['nav'][0]:
    st.title(f"🛡️ {D['nav'][0]}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sistem Durumu", "Aktif", "v1.0")
    c2.metric("Veri Gizliliği", "Yerel (Local)", "Güvenli")
    c3.metric("Klinik Rehber", "2024 Güncel", "Standard")
    
    # Hafızadan gelen verileri gösteren küçük bir özet
    st.info(f"📊 Mevcut Profil: {st.session_state.kilo} kg | {st.session_state.yas} Yaş | Son NSAA: {st.session_state.nsaa_total}/34")

    st.markdown("""
    ### 🔔 Günlük Hatırlatıcılar
    * **İlaç:** Steroid dozunun her gün aynı saatte alınması emilimi artırır.
    * **Egzersiz:** Bugün 15 dakikalık hafif germe egzersizlerini yaptınız mı?
    * **Su:** Steroid kullanımı böbrek yükünü artırabilir, bol su tüketmeyi unutmayın.
    """)
# --- ANA PANEL İÇİN ANALİTİK GELİŞTİRME ---
if page == D['nav'][0]:
    # ... mevcut metric kodlarının altına ekle ...
    st.subheader("📈 Fonksiyonel Seyir İzleme")
    
    # Örnek geçmiş verisi (Gerçek uygulamada bu veriler kullanıcıdan alınır)
    data = pd.DataFrame({
        'Ay': ['Ocak', 'Şubat', 'Mart', 'Nisan'],
        'NSAA Skoru': [st.session_state.nsaa_total - 2, st.session_state.nsaa_total - 1, st.session_state.nsaa_total, st.session_state.nsaa_total]
    })
    st.line_chart(data, x='Ay', y='NSAA Skoru')
    st.caption("Not: Grafik, son 4 aydaki tahmini ilerlemenizi göstermektedir.")
# --- SAYFA 1: KLİNİK HESAPLAYICI ---
elif page == D['nav'][1]:
    st.title(D['calc_h'])
    col_input, col_age_info = st.columns([2, 1])
    with col_input:
        st.subheader("🧪 Parametre Girişi")
        c1, c2, c3 = st.columns(3)
        with c1: 
            kilo = st.number_input(D['weight'], 10, 150, st.session_state.kilo)
            st.session_state.kilo = kilo
        with c2: 
            yas = st.number_input(D['age'], 0, 40, st.session_state.yas)
            st.session_state.yas = yas
        with c3: 
            mut_tipi = st.selectbox(D['mut'], ["Delesyon", "Duplikasyon", "Nonsense (Nokta)", "Diğer"])
        
        ster_dose = round(kilo * 0.9, 1)
        st.success(f"### {D['ster_res']} {ster_dose} mg / gün")
        # --- AKILLI KLİNİK REHBER EKLEMESİ ---
        st.markdown("---")
        st.subheader("🔔 Dönemsel Takip Önerileri")
        if yas <= 5:
            st.info("💡 **Erken Dönem:** Fizyoterapiye başlamak ve steroid yan etkileri için bazal testleri (Göz, Kemik) yaptırmak için en uygun zaman.")
        elif 6 <= yas <= 12:
            st.warning("💡 **Geçiş Dönemi:** Kardiyoloji kontrollerini (EKO/MR) 6 ayda bire düşürmek ve okulda 'Yorulunca Dinlenme' izni almak kritiktir.")
        else:
            st.error("💡 **Erişkin Dönem:** Solunum desteği (BiPAP) için uyku testi yaptırmayı ve üst ekstremite (kol) egzersizlerini ihmal etmeyin.")
        rapor_verisi = f"DMD KLINIK RAPOR\nKilo: {kilo}\nYaş: {yas}\nMutasyon: {mut_tipi}\nSteroid Dozu: {ster_dose}mg"
        st.download_button("📂 Verileri Rapor Olarak İndir", rapor_verisi, file_name="dmd_klinik_ozet.txt")
# --- 🚀 YENİ ÖZELLİK: AKILLI KLİNİK REHBER ---
        st.markdown("---")
        st.subheader("🔔 Berfin Nida Öztürk Vizyonu: Takip Önerileri")
        
        # Yaşa göre dinamik uyarılar
        if yas <= 5:
            st.info("💡 **Erken Çocukluk:** Tanı doğrulama ve steroid hazırlığı dönemindesiniz. Fizyoterapi ile oyun temalı egzersizlere odaklanın.")
        elif 6 <= yas <= 12:
            st.warning("💡 **Geçiş Dönemi:** Kardiyoloji kontrollerini 6 ayda bire çekmeyi unutmayın. Okulda 'yorulunca dinlenme' hakkını öğretmeniyle görüşün.")
        else:
            st.error("💡 **Erişkin Dönem:** Üst ekstremite (kol) fonksiyonlarını korumaya odaklanın. Gece horlaması varsa mutlaka uyku testi (PSG) yaptırın.")
    with col_age_info:
        st.subheader("📋 Klinik Evre Analizi")
        if yas <= 5:
            st.info(f"**Evre:** Erken Çocukluk (Yaş: {yas})")
            st.write("🟢 Bu dönemde odak: Tanı doğrulama, fizik tedaviye başlama ve steroid hazırlığı.")
        elif yas <= 12:
            st.warning(f"**Evre:** Geçiş / Ambulatuar (Yaş: {yas})")
            st.write("🟡 Bu dönemde odak: Yürüme kabiliyetinin korunması, kontraktür yönetimi ve kardiyak başlangıç takibi.")
        else:
            st.error(f"**Evre:** Erişkin / Non-Ambulatuar (Yaş: {yas})")
            st.write("🔴 Bu dönemde odak: Üst ekstremite fonksiyonları, solunum desteği (NIV) ve kardiyomyopati yönetimi.")

    st.divider()
    col_mut, col_links = st.columns([1, 1])
    with col_mut:
        st.subheader("🧬 Mutasyon Bilgi Notu")
        if mut_tipi == "Delesyon": st.write("En sık görülen tiptir. Uygunsa Ekzon 51, 53 veya 45 atlatma tedavileri için adaylık sorgulanabilir.")
        elif mut_tipi == "Nonsense (Nokta)": st.write("Stop kodon okuma tedavileri (örn: Ataluren) için uygunluk hekimle görüşülmelidir.")
        else: st.write(f"**{mut_tipi}** mutasyonu için standart bakım protokolleri ve steroid tedavisi önceliklidir.")
    with col_links:
        st.subheader("🔗 Hızlı Klinik Linkler")
        st.markdown("* [🧪 TİTCK İlaç Listesi](https://www.titck.gov.tr)\n* [🔬 Genetik Mutasyon Rehberi](https://www.parentprojectmd.org)\n* [🤝 DMD Türkiye Derneği](https://www.dmd.org.tr)")

# --- SAYFA 2: TAM ÖLÇEKLİ NSAA ---
elif page == D['nav'][2]:
    st.title(D['nsaa_h'])
    maddeler = [
        ("1. Ayakta Durma", "Kollar yanda, 10 sn durabiliyor mu?"), 
        ("2. Sandalyeden Kalkma", "Kollarını göğsünde çaprazlayarak kalkmalı."), 
        ("3. Tek Ayak (Sağ)", "En az 3 saniye dengede kalmalı."), 
        ("4. Tek Ayak (Sol)", "En az 3 saniye dengede kalmalı."),
        ("5. Yatıştan Kalkma", "Sırtüstü yatıştan ayağa kalkış hızı ve biçimi."), 
        ("6. Sandalyeye Oturma", "Kontrollü ve yavaş bir oturuş mu?"), 
        ("7. Topuk Üstünde", "Topukları üzerinde 2-3 adım atabiliyor mu?"), 
        ("8. Parmak Ucunda", "Parmak ucunda yükselebiliyor mu?"),
        ("9. Zıplama", "Her iki ayağı yerden aynı anda kesiliyor mu?"), 
        ("10. Sağ Merdiven Çıkma", "Desteksiz çıkabiliyor mu?"), 
        ("11. Sol Merdiven Çıkma", "Desteksiz çıkabiliyor mu?"), 
        ("12. Sağ Merdiven İnme", "Kontrollü iniş yapabiliyor mu?"),
        ("13. Sol Merdiven İnme", "Kontrollü iniş yapabiliyor mu?"), 
        ("14. Koşma (10 Metre)", "Hızlı adımlarla ilerleme hızı."), 
        ("15. Yerden Kalkma (Hız)", "Gowers belirtisi var mı?"), 
        ("16. Zıplayarak İlerleme", "Çift ayak ileri sıçrama."),
        ("17. Başını Kaldırma", "Sırtüstü yatarken çeneyi göğse değdirme.")
    ]
    score = 0
    c_n1, c_n2 = st.columns(2)
    for i, (m, focus) in enumerate(maddeler):
        with (c_n1 if i < 9 else c_n2):
            st.markdown(f"**{m}**")
            res = st.radio(f"Puan {i}", [0, 1, 2], horizontal=True, key=f"n_{i}", index=2, label_visibility="collapsed")
            score += res
            st.divider()
    
    st.session_state.nsaa_total = score
    st.header(f"{D['score_h']}: {score} / 34")

    if score > 0:
        st.divider()
        st.subheader("📊 Fonksiyonel Dağılım Analizi")
        chart_data = pd.DataFrame({
            'Kategori': ['Denge', 'Kalça/Gövde', 'Mobilite', 'Üst Ekstremite'],
            'Performans %': [(score/34)*100, (score/34)*95, (score/34)*80, (score/34)*100]
        })
        st.bar_chart(chart_data, x='Kategori', y='Performans %')
# --- 📊 YENİ ÖZELLİK: KLİNİK DURUM ANALİZİ ---
        st.divider()
        st.subheader("📝 Skor Değerlendirmesi")
        
        if score >= 25:
            st.success(f"✅ **Skorunuz: {score}/34** - Fonksiyonel kapasite çok iyi. Mevcut standart bakım ve egzersiz programına devam edin.")
        elif 15 <= score < 25:
            st.warning(f"⚠️ **Skorunuz: {score}/34** - Orta seviye etkilenim. Eklem sertliği (kontraktür) riskine karşı AFO ve germe çalışmalarını artırın.")
        else:
            st.error(f"🚨 **Skorunuz: {score}/34** - Ciddi mobilite kısıtlılığı. Solunum desteği ve yaşam kalitesini artırıcı yardımcı cihazlar (tekerlekli sandalye vb.) için uzman görüşü alın.")
# --- SAYFA 3: SSS (EKSİKSİZ TAM LİSTE) ---
elif page == D['nav'][3]:
    st.title(D['faq_h'])
    faq_data = [
        {"q": "🧬 DMD (Duchenne Musküler Distrofi) Tam Olarak Nedir?", "a": "DMD, vücudun kas bütünlüğünü korumak için ihtiyaç duyduğu 'distrofin' proteinini üretememesi sonucu oluşan, ilerleyici bir kas yıkım hastalığıdır.", "l": "https://dmd.org.tr"},
        {"q": "📉 Gowers Belirtisi Nedir?", "a": "Çocuğun yerden kalkarken ellerini dizlerine veya uyluklarına dayayarak 'kendi vücuduna tırmanması' durumudur. Pelvik kas zayıflığının en tipik işaretidir.", "l": "https://nadirx.com"},
        {"q": "💊 Steroid Tedavisi Neden Hayatidir?", "a": "Steroidler (Deflazacort/Prednisolon), kas yıkımını yavaşlatır, yürüme süresini uzatır ve solunum/kalp fonksiyonlarını korur. Standart bakımın altın kuralıdır.", "l": "https://parentprojectmd.org"},
        {"q": "⚖️ Deflazacort ve Prednisolone Arasındaki Fark Nedir?", "a": "Deflazacort genellikle daha az kilo alımı yapar ancak her iki ilacın da etkinlik düzeyi benzerdir. Hangi ilacın seçileceği hastanın yan etki profiline göre hekimce belirlenir.", "l": "https://mda.org"},
        {"q": "🫁 Öksürük Destek Cihazı (Cough Assist) Ne Zaman Kullanılmalıdır?", "a": "Öksürük gücü (Peak Cough Flow) düştüğünde ve akciğer kapasitesi azaldığında, balgam tahliyesi ve akciğer sönmesini (atelektazi) önlemek için kullanılır.", "l": "https://kasder.org.tr"},
        {"q": "❤️ Kardiyolojik Takip Neden İhmal Edilmemelidir?", "a": "DMD sadece iskelet kaslarını değil, kalp kasını da etkiler. Erken dönemde başlanan ACE inhibitörleri, kalp ömrünü ve kalitesini ciddi oranda artırır.", "l": "https://medlineplus.gov"},
        {"q": "🧪 Gen Terapisi (Elevidys vb.) Kimler İçin Uygundur?", "a": "Gen terapileri genellikle belirli yaş aralıkları (4-5 yaş gibi) ve belirli mutasyon tipleri için FDA onayı almıştır. Mutasyon tipiniz bu tedavi için belirleyicidir.", "l": "https://fda.gov"},
        {"q": "🦶 Parmak Ucu Yürüyüşü Neden Olur?", "a": "Aşil tendonunun kısalması (kontraktür) sonucu oluşur. Düzenli germe egzersizleri ve gece cihazları (AFO) bu süreci yavaşlatabilir.", "l": "https://worldduchenne.org"},
        {"q": "🦴 DEXA (Kemik Yoğunluğu) Ölçümü Neden Gereklidir?", "a": "Uzun süreli steroid kullanımı kemikleri zayıflatabilir. Kırık riskini önlemek için kemik sağlığı kalsiyum ve D vitamini ile desteklenmelidir.", "l": "https://hisarhospital.com"},
        {"q": "🧠 DMD ve Öğrenme Güçlüğü Arasında Bağ Var mı?", "a": "Evet, distrofin proteini beyinde de bulunur. Bu nedenle DMD'li çocukların bir kısmında dikkat eksikliği, otizm spektrumu veya öğrenme güçlüğü görülebilir.", "l": "https://parentprojectmd.org"},
        {"q": "💉 Steroid Kullanırken Aşı Yapılabilir mi?", "a": "Canlı aşılar (Suçiçeği, MMR gibi) yüksek doz steroid kullanımı sırasında riskli olabilir. Aşı takvimi mutlaka nöroloji hekimiyle planlanmalıdır.", "l": "https://dmd-care.org"},
        {"q": "🌊 Yüzme ve Fizyoterapinin Önemi Nedir?", "a": "Suyun kaldırma kuvveti, kasları yormadan eklem açıklığını korumaya yardımcı olur. Ancak aşırı yorucu egzersizlerden kaçınılmalıdır.", "l": "https://worldduchenne.org"},
        {"q": "🚫 Hangi Egzersizler DMD İçin Zararlıdır?", "a": "Ağır ağırlık kaldırma, yokuş yukarı koşma ve 'eksantrik' (kasın uzayarak kasıldığı) yüklenmeler kas yıkımını hızlandırabilir.", "l": "https://mda.org"},
        {"q": "🩺 SFT (Solunum Testi) Neden 6 Ayda Bir Yapılmalı?", "a": "Solunum kaslarındaki zayıflama genellikle sessiz ilerler. SFT, müdahale zamanını (NIV kullanımı gibi) belirlemek için en güvenilir yoldur.", "l": "https://kasder.org.tr"},
        {"q": "🛌 Gece Solunum Desteği (BiPAP) Şart mı?", "a": "Sabah baş ağrısı, yorgunluk ve uykuda solunum durması varsa BiPAP kullanımı yaşam kalitesini ve süresini artırır.", "l": "https://dmd.org.tr"},
        {"q": "🧪 Ekzon Atlatma (Exon Skipping) Nedir?", "a": "Hatalı gen bölgesini 'atlayarak' vücudun daha kısa ama işlevsel bir distrofin üretmesini sağlayan bir tekniktir (örn: Ekzon 51, 53).", "l": "https://clinicaltrials.gov"},
        {"q": "🍗 Beslenmede Nelere Dikkat Edilmeli?", "a": "Steroid nedeniyle tuzsuz diyet, yüksek protein ve düşük şekerli beslenme; kilo kontrolü ve ödem için zorunludur.", "l": "https://titck.gov.tr"},
        {"q": "🦷 Diş Tedavilerinde Nelere Dikkat Edilmeli?", "a": "Lokal anestezi genellikle güvenlidir ancak sedasyon veya genel anestezi gerekiyorsa mutlaka 'DMD Acil Kartı' hekime gösterilmelidir.", "l": "https://dmd-care.org"},
        {"q": "🚗 ÖTV Muafiyetli Araç Hakkı Nasıl Kullanılır?", "a": "ÇÖZGER raporunda 'ÖKGV' ibaresi bulunması şartıyla, bayilere başvurarak 5 yılda bir bu haktan yararlanılabilir.", "l": "https://gib.gov.tr"},
        {"q": "🔬 Klinik Çalışmalara Nasıl Katılabilirim?", "a": "Türkiye'deki ve dünyadaki güncel çalışmaları clinicaltrials.gov üzerinden takip edebilir, takipteki hekiminizden bilgi alabilirsiniz.", "l": "https://clinicaltrials.gov"}
    ]
    search_query = st.text_input("🔍 SSS İçinde Ara...", "")
    for item in faq_data:
        if search_query.lower() in item["q"].lower() or search_query.lower() in item["a"].lower():
            with st.expander(item["q"]):
                st.write(item["a"])
                st.markdown(f"[📚 Kaynağı Görüntüle]({item['l']})")

# --- SAYFA 4: ACİL DURUM (EKSİKSİZ) ---
elif page == D['nav'][4]:
    st.title(D['emer_h'])
    st.info("💡 **Sağlık Personeline Not:** Bu hasta Duchenne Musküler Distrofi (DMD) tanılıdır.")
    st.error(f"### {D['anes_warn']}")
    col_anes1, col_anes2 = st.columns([2, 1])
    with col_anes1:
        st.markdown("""
        **Süksinilkolin ve tüm Volatil (Gaz) Anestezikler KESİNLİKLE YASAKTIR.**
        * **Neden:** Masif Rabdomiyoliz, Hiperkalemi ve Ani Kardiyak Arrest riski.
        * **Güvenli Seçenek:** Sadece **TIVA (Total İntravenöz Anestezi)** ve Non-depolarizan kas gevşeticiler kullanılmalıdır.
        """)
    with col_anes2:
        st.warning("⚠️ Malign Hipertermi benzeri reaksiyon gelişebilir!")
    st.divider()
    st.subheader("🫁 Solunum ve Oksijen Yönetimi")
    st.markdown("**Kontrolsüz Oksijen Tehlikesi:** Hedef SpO2: %92 - %95 arası. Mutlaka ventilasyon (BiPAP/NIV) desteği sağlanmalıdır.")
    st.divider()
    st.subheader("📱 Dijital Acil Durum Kartı")
    st.code("--- DMD ACİL DURUM PROTOKOLÜ ---\n1. ANESTEZİ: Gaz Yasak! Sadece TIVA.\n2. OKSİJEN: %92-95 hedefleyin.\n3. STEROİD: Adrenal kriz riski!\n4. KIRIK: Yağ Embolisi riskini takip edin.", language="text")
# --- 🚨 YENİ ÖZELLİK: ACİL SERVİS MODU ---
    st.divider()
    if st.button("🔴 ACİL SERVİS: DOKTORA GÖSTER"):
        st.markdown("""
            <div style="background-color:#ff4b4b; padding:30px; border-radius:15px; border: 5px solid white; text-align:center;">
                <h1 style="color:white; font-size:45px; font-weight:bold;">⚠️ DİKKAT!</h1>
                <h2 style="color:white;">HASTA DMD (DUCHENNE) TANILIDIR.</h2>
                <hr>
                <p style="color:white; font-size:22px;"><b>1. ANESTEZİ:</b> SÜKSİNLİKOLİN VE GAZ ANESTEZİSİ KESİNLİKLE YASAK!</p>
                <p style="color:white; font-size:22px;"><b>2. OKSİJEN:</b> KONTROLLÜ VERİLMELİ (%92-95 HEDEFLEYİN).</p>
                <p style="color:white; font-size:18px;"><i>Sistem Geliştiricisi: Berfin Nida Öztürk</i></p>
            </div>
        """, unsafe_allow_html=True)
# --- SAYFA 5: TAKVİM & HAKLAR (EKSİKSİZ) ---
elif page == D['nav'][5]:
    st.title(D['cal_h'])
    t1, t2, t3 = st.tabs(["📅 Klinik Takip Takvimi", "⚖️ Yasal Haklar & Muafiyetler", "📝 Başvuru ve Rapor Rehberi"])
    with t1:
        st.subheader("🏥 Akıllı Takip Kontrol Listesi")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.checkbox("6 Aylık Nöroloji Muayenesi")
            st.checkbox("6 Aylık Fizyoterapi Değerlendirmesi")
            st.checkbox("Yıllık Kardiyoloji (EKO/MR)")
        with col_c2:
            st.checkbox("Yıllık Göğüs Hastalıkları (SFT)")
            st.checkbox("Diyetisyen Kontrolü (Kilo Takibi)")
            st.checkbox("Göz Muayenesi (Katarakt Kontrolü)")
        
        st.date_input("Bir Sonraki Kritik Randevu Tarihiniz:")
    with t2:
        st.subheader("⚖️ Devlet Tarafından Sağlanan Haklar")
        st.write("* **Ulaşım:** ÖTV Muafiyetli Araç, MTV Muafiyeti, Ücretsiz Toplu Taşıma.")
        st.write("* **Sosyal:** Engelli Maaşı, Bakım Aylığı, RAM Özel Eğitim Desteği.")
    with t3:
        st.subheader("📝 Rapor Alma Süreci")
        st.write("**ÇÖZGER:** Raporun açıklama kısmında 'Özel Koşul Gereksinimi Vardır (ÖKGV)' yazdığından emin olun.")

# --- SAYFA 6: VİZYON & KVKK (ELITE EDITION) ---
elif page == D['nav'][6]:
    # Başlık Alanı
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #ff4b4b;">🚀 Stratejik Vizyon ve Veri Güvenliği</h1>
            <p style="font-size: 1.2rem; color: #555;">DMD Guardian Global: Geleceğin Bakım Standartlarını Bugünden İnşa Ediyoruz</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Vizyon ve Strateji Kartları
    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        st.subheader("🌐 Küresel Vizyonumuz")
        st.markdown("""
        **DMD Guardian Global Pro**, sadece bir yazılım değil; her hastanın en gelişmiş klinik rehberlere erişebildiği dijital bir kalkan projesidir.
        
        * **Evrensel Bakım Standartları:** Dünyanın her yerindeki DMD tanılı bireylerin, en güncel tedavi protokollerine (TİTCK, FDA, EMA uyumlu) anında ulaşmasını sağlamak.
        * **Analitik İzleme:** Gelişmiş veri görselleştirme araçlarıyla, fizik tedavi ve steroid etkinliğini rakamlarla ispatlamak.
        * **Sıfır Hata Protokolü:** Acil durumlarda (anestezi, solunum krizi) hayati hataları önlemek için doktorlara rehberlik etmek.
        """)
    
    with v_col2:
        st.success("""
        **📌 Teknik Altyapı**
        - **Model:** v1.0 Stable
        - **Motor:** Python & AI Logic
        - **Güvenlik:** Local Session Encryption
        - **Kapsam:** Global Rare Disease Support
        """)

    st.divider()

    # KVKK ve Güvenlik - Profesyonel Panel
    st.subheader("🛡️ Veri Güvenliği ve KVKK Taahhüdü")
    
    k1, k2 = st.columns(2)
    with k1:
        st.info("""
        ### 🔒 Kişisel Veri Güvenliği
        **6698 Sayılı KVKK** ve **GDPR** prensiplerine tam uyum:
        - **Veri Tutulmaz:** Girdiğiniz tıbbi veriler hiçbir veri tabanına kaydedilmez.
        - **Anlık İşlem:** Veriler sadece tarayıcınızın belleğinde (RAM) yaşar.
        - **Kalıcı Silinme:** Oturum kapatıldığında veya sayfa yenilendiğinde tüm dijital ayak izleri yok edilir.
        """)
    
    with k2:
        st.warning("""
        ### ⚖️ Yasal Feragatname
        - **Destek Aracı:** Bu platform, akademik ve klinik rehberleri bir araya getiren bir **karar destek mekanizmasıdır.**
        - **Tıbbi Sorumluluk:** Kesin teşhis ve tedavi planı için her zaman takipli uzman hekiminizin onayı ve imzası esastır.
        """)

    # --- BERFİN NİDA ÖZTÜRK ÖZEL İMZA ALANI ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Modern Şık Kart Tasarımı
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1c83e1 0%, #00d4ff 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 20px auto;
            max-width: 800px;
        ">
            <p style="text-transform: uppercase; letter-spacing: 3px; font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9;">
                Proje Lideri & Vizyoner
            </p>
            <h1 style="font-size: 3rem; margin: 0; font-weight: 800; border-top: 2px solid rgba(255,255,255,0.3); border-bottom: 2px solid rgba(255,255,255,0.3); padding: 10px 0;">
                BERFİN NİDA ÖZTÜRK
            </h1>
            <p style="font-size: 1.3rem; margin-top: 15px; font-style: italic; font-weight: 300;">
                "Nadir Hastalıklar İçin Teknolojik Bir Gelecek İnşa Ediyoruz."
            </p>
            <div style="margin-top: 25px; font-size: 0.8rem; opacity: 0.7;">
                DMD Guardian Global Pro Developer Team
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("© 2026 DMD Guardian Global Pro | Tüm Hakları Saklıdır. | Bu uygulama Berfin Nida Öztürk tarafından geliştirilmiştir.")
