import streamlit as st
import pandas as pd

# 1. SAYFA VE DİL YAPILANDIRMASI
st.set_page_config(page_title="DMD Guardian Global Pro", layout="wide", initial_sidebar_state="expanded")

# --- DİL SİSTEMİ (SESSION STATE) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'TR'

def switch_lang():
    st.session_state.lang = 'EN' if st.session_state.lang == 'TR' else 'TR'

# Sidebar dil butonu
st.sidebar.button("🌐 TR / EN - Change Language", on_click=switch_lang)

# Metin Sözlüğü
D = {
    'TR': {
        'nav': ["Ana Panel / Dashboard", "Tam Ölçekli NSAA Testi", "Genişletilmiş SSS / FAQ", "Klinik Takvim & Yasal Haklar", "Acil Durum & Solunum"],
        'anes_warn': "🚨 KRİTİK: Anestezi Uyarısı!",
        'ster_warn': "Steroidler Asla Aniden Kesilmemelidir!",
        'calc_h': "🧬 Klinik Hesaplayıcı & Veri Girişi",
        'weight': "Kilo (kg)",
        'age': "Yaş",
        'mut': "Mutasyon Tipi",
        'ster_res': "**Günlük Steroid Dozaj Tahmini (Deflazacort):**",
        'nsaa_h': "🏃 Klinik Kuzey Yıldızı (NSAA) Gelişmiş Takip",
        'score_h': "📊 Toplam NSAA Skoru",
        'faq_h': "❓ Sık Sorulan Sosular & Akademik Rehber",
        'cal_h': "🏥 Klinik Takvim & Kapsamlı Yasal Haklar",
        'emer_h': "🚨 Acil Durum & Kritik Bakım Yönetimi"
    },
    'EN': {
        'nav': ["Dashboard", "Full Scale NSAA Test", "Extended FAQ", "Clinical Calendar & Rights", "Emergency & Respiratory"],
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
page = st.sidebar.radio("Menu", D['nav'])
st.sidebar.divider()
st.sidebar.error(D['anes_warn'])
st.sidebar.warning(D['ster_warn'])

# --- SAYFA 1: ANA PANEL (DİNAMİK) ---
if page == D['nav'][0]:
    st.title(f"🛡️ {D['nav'][0]}")
    col_input, col_age_info = st.columns([2, 1])
    with col_input:
        st.subheader(D['calc_h'])
        c1, c2, c3 = st.columns(3)
        with c1: kilo = st.number_input(D['weight'], 10, 150, 30)
        with c2: yas = st.number_input(D['age'], 0, 40, 6)
        with c3: mut_tipi = st.selectbox(D['mut'], ["Delesyon", "Duplikasyon", "Nonsense (Nokta)", "Diğer"])
        st.success(f"{D['ster_res']} {round(kilo*0.9, 1)} mg")
        
        

    with col_age_info:
        st.info(f"📅 **{yas} {D['age']}**")
        if yas <= 5: st.write("Erken evre / Early Stage")
        elif yas <= 12: st.write("Geçiş evresi / Transition")
        else: st.write("Erişkin evre / Adult")
    
    st.divider()
    st.subheader("🔗 Klinik Linkler")
    st.markdown("[🧪 TİTCK](https://www.titck.gov.tr) | [🤝 DMD Türkiye](https://www.dmd.org.tr) | [🔬 ClinicalTrials](https://clinicaltrials.gov)")

# --- SAYFA 2: TAM ÖLÇEKLİ NSAA ---
elif page == D['nav'][1]:
    st.title(D['nsaa_h'])
    
    
    
    maddeler = [
        ("1. Ayakta Durma", "Denge / Postüral Kontrol"), ("2. Sandalyeden Kalkma", "Kalça Ekstansörleri"),
        ("3. Tek Ayak (Sağ)", "Pelvik Stabilite"), ("4. Tek Ayak (Sol)", "Pelvik Stabilite"),
        ("5. Yatıştan Kalkma", "Gowers Manevrası"), ("6. Sandalyeye Oturma", "Eksantrik Kontrol"),
        ("7. Topuk Üstünde", "Distal Güç"), ("8. Parmak Ucunda", "Baldır Gücü"),
        ("9. Zıplama", "Patlayıcı Güç"), ("10. Sağ Merdiven Çıkma", "Mobilite"),
        ("11. Sol Merdiven Çıkma", "Mobilite"), ("12. Sağ Merdiven İnme", "Kontrol"),
        ("13. Sol Merdiven İnme", "Kontrol"), ("14. Koşma (10 Metre)", "Sürat"),
        ("15. Yerden Kalkma (Hız)", "Zamanlı Test"), ("16. Zıplayarak İlerleme", "Koordinasyon"),
        ("17. Başını Kaldırma", "Boyun Gücü")
    ]
    score, res_list = 0, []
    c_n1, c_n2 = st.columns(2)
    for i, (m, focus) in enumerate(maddeler):
        with (c_n1 if i < 9 else c_n2):
            st.markdown(f"**{m}**")
            st.caption(f"🎯 {focus}")
            res = st.radio(f"Puan {i}", [0, 1, 2], horizontal=True, key=f"n_{i}", index=2, label_visibility="collapsed")
            score += res
            res_list.append(res)
            if "Koşma" in m or "Yerden Kalkma" in m or "Merdiven" in m:
                st.number_input(f"Süre/Time (sn) - {m}", 0.0, 60.0, 0.0, key=f"t_{i}")
            st.divider()

    st.header(f"{D['score_h']}: {score} / 34")
    prox, dist, mobi = sum(res_list[0:6]), sum(res_list[6:10]), sum(res_list[10:17])
    h1, h2, h3 = st.columns(3)
    h1.metric("Proksimal", f"{prox}/12")
    h2.metric("Distal", f"{dist}/8")
    h3.metric("Mobilite", f"{mobi}/14")
    
    chart_data = pd.DataFrame({"Zone": ["Proximal", "Distal", "Mobility"], "Score %": [(prox/12)*100, (dist/8)*100, (mobi/14)*100]})
    st.bar_chart(chart_data, x="Zone", y="Score %")

# --- SAYFA 3: SSS (20 MADDE EKSİKSİZ) ---
elif page == D['nav'][2]:
    st.title(D['faq_h'])
    faq_items = [
        {"q": "🧬 DMD Nedir?", "a": "Distrofin eksikliği sonucu kas yıkımıdır.", "l": "https://dmd.org.tr"},
        {"q": "📉 Gowers Belirtisi?", "a": "Yerden kalkarken bacaklardan destek alma.", "l": "https://nadirx.com"},
        {"q": "💊 Steroidlerin Rolü?", "a": "Gücü korur, süreci uzatır.", "l": "https://parentprojectmd.org"},
        {"q": "⚖️ Deflazacort vs Prednisolone?", "a": "Yan etki profilleri farklıdır.", "l": "https://mda.org"},
        {"q": "🫁 Cough Assist?", "a": "Balgam atmayı ve akciğeri korur.", "l": "https://kasder.org.tr"},
        {"q": "❤️ Kalp İlaçları?", "a": "ACE inhibitörleri kalp ömrünü uzatır.", "l": "https://medlineplus.gov"},
        {"q": "🧪 Gen Terapisi?", "a": "Mikro-distrofin gen aktarımıdır.", "l": "https://fda.gov"},
        {"q": "🦶 Parmak Ucu Yürüyüşü?", "a": "Tendon kısalması sonucu oluşur.", "l": "https://worldduchenne.org"},
        {"q": "🦴 DEXA Ölçümü?", "a": "Kemik yoğunluğu takibi içindir.", "l": "https://hisarhospital.com"},
        {"q": "🧠 Öğrenme Güçlüğü?", "a": "DMD'li çocukların %30'unda görülebilir.", "l": "https://parentprojectmd.org"},
        {"q": "💉 Aşılar?", "a": "Canlı aşılar steroidle riskli olabilir.", "l": "https://dmd-care.org"},
        {"q": "🌊 Yüzme?", "a": "Eklemleri yormadan kasları çalıştırır.", "l": "https://worldduchenne.org"},
        {"q": "🚫 Yasak Egzersizler?", "a": "Ağır ağırlık ve eksantrik yüklenme.", "l": "https://mda.org"},
        {"q": "🩺 SFT Testi?", "a": "Akciğer kapasitesini ölçer.", "l": "https://kasder.org.tr"},
        {"q": "🛌 Gece Cihazı (NIV)?", "a": "Uykuda solunum desteği sağlar.", "l": "https://dmd.org.tr"},
        {"q": "🧪 Ekzon Atlatma?", "a": "Hatalı gen bölgesini bypass eder.", "l": "https://clinicaltrials.gov"},
        {"q": "🍗 Beslenme?", "a": "Tuzsuz ve dengeli diyet şarttır.", "l": "https://titck.gov.tr"},
        {"q": "🦷 Diş Tedavisi?", "a": "Anestezi uyarısı dişçiye iletilmelidir.", "l": "https://dmd-care.org"},
        {"q": "🚗 ÖTV Muafiyeti?", "a": "ÇÖZGER ÖKGV ibaresi gereklidir.", "l": "https://gib.gov.tr"},
        {"q": "🔬 Klinik Çalışmalar?", "a": "Clinicaltrials.gov üzerinden takip edilebilir.", "l": "https://clinicaltrials.gov"}
    ]
    for item in faq_items:
        with st.expander(item["q"]):
            st.write(item["a"])
            st.markdown(f"[🔗 Detaylı Kaynak]({item['l']})")

# --- SAYFA 4: KLİNİK TAKVİM & HAKLAR (STRATEJİK REHBER) ---
elif page == D['nav'][3]:
    st.title(D['cal_h'])
    
    t1, t2, t3 = st.tabs(["📅 Klinik Takip Takvimi", "⚖️ Yasal Haklar ve Sosyal Destek", "📝 Adım Adım Başvuru Rehberi"])
    
    with t1:
        st.subheader("⏱️ Periyodik Randevu ve Test Yönetimi")
        
        
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.info("### **6 Ayda Bir (Rutin Kontrol)**")
            st.markdown("""
            * **Pediatrik Nöroloji:** NSAA motor değerlendirmesi, fonksiyonel takip ve **Steroid doz ayarı** (Kilo artışına göre hassas ayar).
            * **Fizyoterapi:** Eklem kontraktür riski için ROM (Eklem hareket açıklığı) ölçümü, ev programı revizyonu ve cihaz (AFO) kontrolü.
            """)
            
            st.warning("### **Yılda Bir (Kritik Taramalar)**")
            st.markdown("""
            * **Kardiyoloji (EKO/MR):** Kardiyomiyopati (kalp kası zayıflığı) tespiti için hayati önemdedir.
            * **Göğüs Hastalıkları (SFT):** Akciğer kapasitesi ölçümü. Gerekirse Cough Assist veya solunum desteği planlaması.
            """)

        with col_t2:
            st.success("### **Ek ve Destekleyici Branşlar**")
            st.markdown("""
            * **Endokrinoloji (DEXA):** Steroid kullanımına bağlı kemik yoğunluğu kaybı ve D vitamini takibi.
            * **Göz Muayenesi:** Steroid kaynaklı katarakt veya göz tansiyonu riski kontrolü.
            * **Beslenme/Diyet:** Steroid ödemi, kilo kontrolü ve sodyum (tuzsuz) diyet yönetimi.
            * **Ortopedi:** Omurga eğriliği (Skolyoz) ve kalça çıkığı kontrolleri.
            """)

    with t2:
        st.subheader("⚖️ Devlet Destekleri ve Sosyal Haklar")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("#### 🚗 **Ulaşım ve Vergi Hakları**")
            st.write("- **ÖTV Muafiyetli Araç:** 5 yılda bir araç alım hakkı (ÇÖZGER raporundaki 'Özel Koşul' ibaresi şarttır).")
            st.write("- **MTV Muafiyeti:** Engelli araçları için Motorlu Taşıtlar Vergisi muafiyeti.")
            st.write("- **Ücretsiz Ulaşım:** Belediye otobüsleri, metro ve Marmaray ücretsiz kullanımı.")
            st.write("- **TCDD ve THY İndirimleri:** Trenlerde ücretsiz, uçuşlarda ise %20-40 indirimli bilet.")

        with col_h2:
            st.markdown("#### 🎓 **Eğitim ve Yaşam Hakları**")
            st.write("- **RAM Desteği:** Haftalık ücretsiz fizik tedavi ve özel eğitim seansları.")
            st.write("- **Okul Avantajları:** Giriş kat sınıf, asansör erişimi, sınavda ek süre ve BEP programı.")
            st.write("- **Elektrik/Su/İnternet:** Engelli raporuyla başvurularak faturalarda %30-50 arası indirim.")
            st.write("- **Evde Bakım Maaşı:** Hane halkı gelir kriterine göre bağlanan aylık maddi destek.")

    with t3:
        st.subheader("📝 Başvuru Süreci Yol Haritası")
        
        st.markdown("""
        1.  **ÇÖZGER Raporu (Hayati Adım):** Tam teşekküllü bir hastaneden randevu alın. Raporda mutlaka **'Özel Koşul Gereksinimi Vardır' (ÖKGV)** ibaresinin bulunması, haklardan tam yararlanmanızı sağlar.
        2.  **RAM Kaydı:** ÇÖZGER raporuyla Rehberlik Araştırma Merkezi'ne giderek eğitsel rapor alın. Bu raporla haftalık ücretsiz fizik tedavi seansları başlar.
        3.  **Engelli Kimlik Kartı:** Aile ve Sosyal Hizmetler İl Müdürlüğü'ne başvurarak kartınızı alın. Ulaşım ve indirimler için bu kart gereklidir.
        4.  **Vergi Dairesi:** Araç alımı için ÇÖZGER raporunun aslı gibidir örneğiyle vergi dairesine müracaat ederek onay alın.
        """)
        
        st.info("💡 **Önemli İpucu:** Tüm tıbbi epikrizlerinizi, genetik raporunuzu ve ÇÖZGER raporunuzu her zaman dijital bir klasörde (Google Drive/iCloud) hazır bulundurun.")

# --- SAYFA 5: ACİL DURUM & SOLUNUM (ULTIMATE PROTOCOL) ---
elif page == D['nav'][4]:
    st.title(D['emer_h'])
    
    # SAĞLIK PERSONELİ İÇİN HIZLI NOT
    st.info("💡 **Sağlık Personeline:** Bu hasta Duchenne Musküler Distrofi (DMD) tanılıdır. Aşağıdaki protokoller uluslararası 'DMD Care Considerations' rehberine uygundur.")

    # 1. EN KRİTİK UYARI: ANESTEZİ
    st.error("""
    ## ⚠️ ANESTEZİ YÖNETİMİ (HAYATİ)
    **Süksinilkolin ve tüm Volatil (Gaz) Anestezikler KONTRENDİKEDİR.**
    * **Risk:** Masif Rabdomiyoliz, Hiperkalemi ve Ani Kardiyak Arrest.
    * **Güvenli Seçenek:** Sadece **TIVA (Total İntravenöz Anestezi)** ve Non-depolarizan kas gevşeticiler kullanılmalıdır.
    """)
    
    

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        # 2. STEROİD VE ADRENAL YETMEZLİK
        st.subheader("💊 Steroid ve Adrenal Yönetim")
        st.warning("""
        **Adrenal Kriz Riski:** Hasta kronik steroid kullanıcısıdır. Stres anında vücut yeterli kortizol üretemez.
        * **Stres Dozu:** Ameliyat, ağır enfeksiyon veya ciddi yaralanma durumlarında 'Hidrokortizon Stres Dozu' uygulanmalıdır.
        * **Kritik:** Steroidler asla aniden kesilmemelidir.
        """)
        
        # 3. KIRIK VE YAĞ EMBOLİSİ
        st.subheader("🦴 Ortopedik Aciller")
        st.write("""
        * **Yağ Embolisi Sendromu (FES):** Özellikle tekerlekli sandalye kullanan hastalarda, basit bir düşme veya uzun kemik kırığı sonrası gelişebilir. 
        * **Belirtiler:** Ani solunum sıkıntısı, konfüzyon veya peteşi (küçük kırmızı lekeler). Bu durumda hemen yoğun bakım desteği gerekir.
        """)

    with c2:
        # 4. SOLUNUM VE OKSİJEN YÖNETİMİ
        st.subheader("🫁 Solunum ve Oksijen")
        st.markdown("""
        **Oksijen Tehlikesi:** Solunum dürtüsü zayıf olan DMD hastalarına kontrolsüz yüksek akışlı oksijen verilmesi **CO2 Narkozuna (Solunumun durmasına)** neden olabilir.
        * **Hedef SpO2:** %92 - %95 arası.
        * **Müdahale:** Oksijen desteği verilirken mutlaka ventilasyon (BiPAP/NIV) desteği de düşünülmelidir.
        """)
        
        

        st.success("""
        **Öksürük Desteği (Cough Assist):**
        Balgam atma yeteneği zayıf olduğu için manuel öksürük desteği veya cihazlı öksürük desteği enfeksiyonların zatürreye çevirmesini engeller.
        """)

    st.divider()

    # 5. LABORATUVAR VE KALP NOTLARI
    st.subheader("🧪 Laboratuvar ve Kardiyak Uyarılar")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.write("""
        * **CK ve Karaciğer Enzimleri:** DMD hastalarında CK, AST ve ALT değerleri bazal olarak çok yüksektir (10.000+). Bu durum karaciğer yetmezliği veya hepatit ile karıştırılmamalıdır.
        """)
    with col_l2:
        st.write("""
        * **Kardiyomiyopati:** Acil cerrahi öncesi hastanın ejeksiyon fraksiyonu (EF) mutlaka kontrol edilmeli, anestezist kalp yükünü buna göre ayarlamalıdır.
        """)
        
        

    # HIZLI ERİŞİM KARTI (KOPYALANABİLİR)
    st.code("""
    --- DMD ACİL KART ---
    ANESTEZİ: Sadece TIVA (Gaz Yasak!)
    STEROİD: Stres dozu uygulansın.
    OKSİJEN: %92-95 hedef (CO2 takibi yap).
    KIRIK: Yağ embolisine dikkat!
    ----------------------
    """, language="text")