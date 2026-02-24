from coaching.models import Subject, Topic, CoachingConfig
from students.models import Student
from django.db import transaction

def run_rescue_logic(stdout=None):
    """
    Core rescue logic to populate the database with FULL LGS curriculum.
    """
    def log(msg):
        if stdout:
            stdout.write(msg)
        print(msg)

    log("--- STARTING ULTIMATE CURRICULUM RESCUE ---")
    
    curr_data = {
        "Matematik": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Pozitif Tam Sayıların Çarpanları", "Asal Çarpanlara Ayırma"]}, {"week": 2, "topics": ["En Büyük Ortak Bölen (EBOB)", "En Küçük Ortak Kat (EKOK)"]}, {"week": 3, "topics": ["EBOB Problemleri", "EKOK Problemleri"]}, {"week": 4, "topics": ["Aralarında Asal Olma Kuralı"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Tam Sayıların Tam Sayı Kuvvetleri"]}, {"week": 2, "topics": ["Üslü İfadelerle İlgili Temel Kurallar"]}, {"week": 3, "topics": ["Sayıların Ondalık Gösterimi", "Çözümleme"]}, {"week": 4, "topics": ["Bilimsel Gösterim"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Kareköklü İfadeler"]}, {"week": 2, "topics": ["Tam Kare Sayılar"]}, {"week": 3, "topics": ["Kareköklü İfadelerde Çarpma/Bölme"]}, {"week": 4, "topics": ["Kareköklü İfadelerde Toplama/Çıkarma"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Gerçek Sayılar"]}, {"week": 2, "topics": ["Veri Analizi (Çizgi ve Sütun Grafikleri)"]}, {"week": 3, "topics": ["Veri Analizi (Daire Grafiği)"]}, {"week": 4, "topics": ["Basit Olayların Olma Olasılığı"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Cebirsel İfadeler"]}, {"week": 2, "topics": ["Cebirsel İfadeleri Çarpanlara Ayırma"]}, {"week": 3, "topics": ["Özdeşlikler"]}, {"week": 4, "topics": ["Doğrusal Denklemler (Koordinat Sistemi)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Doğrusal İlişkiler"]}, {"week": 2, "topics": ["Eğim"]}, {"week": 3, "topics": ["Eşitsizlikler"]}, {"week": 4, "topics": ["Üçgenler (Yardımcı Elemanlar)"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Üçgen Eşitsizliği"]}, {"week": 2, "topics": ["Pisagor Bağıntısı"]}, {"week": 3, "topics": ["Eşlik ve Benzerlik"]}, {"week": 4, "topics": ["Dönüşüm Geometrisi (Öteleme, Yansıma)"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Geometrik Cisimler (Prizmalar)"]}, {"week": 2, "topics": ["Dik Dairesel Silindir"]}, {"week": 3, "topics": ["Silindirin Hacmi"]}, {"week": 4, "topics": ["Dik Piramit ve Koni"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Eşitsizlikler Genel Tekrar"]}, {"week": 2, "topics": ["Geometri Genel Tekrar"]}, {"week": 3, "topics": ["MEB Örnek Sorular Çözümü"]}, {"week": 4, "topics": ["Deneme Sınavı Analizi"]} ]}, 
            { "id": 6, "weeks": [ {"week": 1, "topics": ["LGS Genel Tekrar - 1"]}, {"week": 2, "topics": ["LGS Genel Tekrar - 2"]}, {"week": 3, "topics": ["Motivasyon ve Stres Yönetimi"]}, {"week": 4, "topics": ["Büyük Gün Hazırlığı"]} ]}
        ],
        "Fen Bilimleri": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Mevsimlerin Oluşumu"]}, {"week": 2, "topics": ["İklim ve Hava Hareketleri"]}, {"week": 3, "topics": ["Küresel İklim Değişikliği"]}, {"week": 4, "topics": ["DNA ve Genetik Kod"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Kalıtım (Mendel Genetiği)"]}, {"week": 2, "topics": ["Mutasyon ve Modifikasyon"]}, {"week": 3, "topics": ["Adaptasyon"]}, {"week": 4, "topics": ["Biyoteknoloji"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Basınç (Katı Basıncı)"]}, {"week": 2, "topics": ["Sıvı Basıncı"]}, {"week": 3, "topics": ["Gaz Basıncı"]}, {"week": 4, "topics": ["Periyodik Sistem"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Fiziksel ve Kimyasal Değişimler"]}, {"week": 2, "topics": ["Kimyasal Tepkimeler"]}, {"week": 3, "topics": ["Asitler ve Bazlar"]}, {"week": 4, "topics": ["Maddenin Isı ile Etkileşimi"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Basit Makineler (Makaralar)"]}, {"week": 2, "topics": ["Kaldıraçlar"]}, {"week": 3, "topics": ["Eğik Düzlem ve Çıkrık"]}, {"week": 4, "topics": ["Basit Makineler (Dişli Çarklar, Kasnaklar)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Besin Zinciri ve Enerji Akışı"]}, {"week": 2, "topics": ["Enerji Dönüşümleri (Fotosentez)"]}, {"week": 3, "topics": ["Enerji Dönüşümleri (Solunum)"]}, {"week": 4, "topics": ["Madde Döngüleri"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Elektrik Yükleri ve Elektriklenme"]}, {"week": 2, "topics": ["Elektrik Yüklü Cisimler"]}, {"week": 3, "topics": ["Elektrik Enerjisinin Dönüşümü"]}, {"week": 4, "topics": ["Sürdürülebilir Kalkınma"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Elektrik Yükleri (Tekrar)"]}, {"week": 2, "topics": ["Çevre Bilimi ve İklim Değişikliği"]}, {"week": 3, "topics": ["DNA ve Genetik Kod (Tekrar)"]}, {"week": 4, "topics": ["Basınç (Tekrar)"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Basit Makineler Genel Tekrar"]}, {"week": 2, "topics": ["Madde ve Endüstri Genel Tekrar"]}, {"week": 3, "topics": ["Fen Bilimleri Deneme 1"]}, {"week": 4, "topics": ["Fen Bilimleri Deneme 2"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Son Genel Tekrar - Fizik"]}, {"week": 2, "topics": ["Son Genel Tekrar - Kimya/Biyoloji"]}, {"week": 3, "topics": ["Çıkmış Sorular Çözümü"]}, {"week": 4, "topics": ["Sınav Stratejileri"]} ]}
        ],
        "Türkçe": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Fiilimsiler (İsim-Fiil)"]}, {"week": 2, "topics": ["Fiilimsiler (Sıfat-Fiil)"]}, {"week": 3, "topics": ["Fiilimsiler (Zarf-Fiil)"]}, {"week": 4, "topics": ["Sözcükte Anlam"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Cümlenin Ögeleri (Temel Ögeler)"]}, {"week": 2, "topics": ["Cümlenin Ögeleri (Yardımcı Ögeler)"]}, {"week": 3, "topics": ["Cümle Vurgusu"]}, {"week": 4, "topics": ["Paragrafta Anlam"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Fiilde Çatı (Özne-Yüklem)"]}, {"week": 2, "topics": ["Fiilde Çatı (Nesne-Yüklem)"]}, {"week": 3, "topics": ["Cümle Türleri (Anlamına Göre)"]}, {"week": 4, "topics": ["Cümle Türleri (Yapısına Göre)"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Yazım Kuralları"]}, {"week": 2, "topics": ["Noktalama İşaretleri"]}, {"week": 3, "topics": ["Metin Türleri"]}, {"week": 4, "topics": ["Söz Sanatları"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Anlatım Bozuklukları (Ögeler)"]}, {"week": 2, "topics": ["Anlatım Bozuklukları (Anlam)"]}, {"week": 3, "topics": ["Paragraf (Ana Düşünce)"]}, {"week": 4, "topics": ["Paragraf (Yardımcı Düşünce)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Sözel Mantık (Giriş)"]}, {"week": 2, "topics": ["Sözel Mantık (Tablo Okuma)"]}, {"week": 3, "topics": ["Grafik ve Görsel Yorumlama"]}, {"week": 4, "topics": ["Deyimler ve Atasözleri"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Paragrafta Yapı"]}, {"week": 2, "topics": ["Sözel Mantık (İleri Seviye)"]}, {"week": 3, "topics": ["Yazım ve Noktalama Tekrar"]}, {"week": 4, "topics": ["Fiilimsiler Tekrar"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Cümlenin Ögeleri Tekrar"]}, {"week": 2, "topics": ["Cümle Türleri Tekrar"]}, {"week": 3, "topics": ["Türkçe Genel Deneme"]}, {"week": 4, "topics": ["Paragraf Hızlandırma Taktikleri"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Sözel Mantık Çıkmış Sorular"]}, {"week": 2, "topics": ["Dil Bilgisi Karma Tekrar"]}, {"week": 3, "topics": ["MEB Örnek Sorular"]}, {"week": 4, "topics": ["Deneme Analizi"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Son Bakış: Yazım Kuralları"]}, {"week": 2, "topics": ["Son Bakış: Noktalama"]}, {"week": 3, "topics": ["Motivasyon"]}, {"week": 4, "topics": ["Sınav Hazırlığı"]} ]}
        ],
        "T.C. İnkılap Tarihi": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Bir Kahraman Doğuyor"]}, {"week": 2, "topics": ["Milli Uyanış"]}, {"week": 3, "topics": ["Milli Mücadele Hazırlık"]}, {"week": 4, "topics": ["TBMM'nin Açılması"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Doğu ve Güney Cepheleri"]}, {"week": 2, "topics": ["Batı Cephesi"]}, {"week": 3, "topics": ["Sakarya Meydan Savaşı"]}, {"week": 4, "topics": ["Büyük Taarruz"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Atatürkçülük ve Türk İnkılabı"]}, {"week": 2, "topics": ["Siyasi Alanda İnkılaplar"]}, {"week": 3, "topics": ["Hukuk Alanında İnkılaplar"]}, {"week": 4, "topics": ["Eğitim Alanında İnkılaplar"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Toplumsal Alanda İnkılaplar"]}, {"week": 2, "topics": ["Ekonomi Alanında İnkılaplar"]}, {"week": 3, "topics": ["Atatürk Dönemi Türk Dış Politikası"]}, {"week": 4, "topics": ["Atatürk'ün Ölümü ve Sonrası"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Demokratikleşme Çabaları"]}, {"week": 2, "topics": ["Atatürk Dönemi Dış Politika (1923-1930)"]}, {"week": 3, "topics": ["Atatürk Dönemi Dış Politika (1930-1938)"]}, {"week": 4, "topics": ["Atatürk'ün Ölümü ve Yankıları"]} ]}, 
            { "id": 2, "weeks": [ {"week": 1, "topics": ["İkinci Dünya Savaşı ve Türkiye"]}, {"week": 2, "topics": ["Çok Partili Hayata Geçiş"]}, {"week": 3, "topics": ["Genel Tekrar: Ünite 1"]}, {"week": 4, "topics": ["Genel Tekrar: Ünite 2"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Genel Tekrar: Milli Mücadele"]}, {"week": 2, "topics": ["Genel Tekrar: İnkılaplar"]}, {"week": 3, "topics": ["Harita Yorumlama"]}, {"week": 4, "topics": ["Kronoloji Çalışması"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Kavram Bilgisi (Siyasi, Hukuki)"]}, {"week": 2, "topics": ["Kavram Bilgisi (Sosyal, Ekonomik)"]}, {"week": 3, "topics": ["Örnek Sorular Çözümü"]}, {"week": 4, "topics": ["Deneme Sınavı 1"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["T.C. İnkılap Tarihi Deneme 2"]}, {"week": 2, "topics": ["Çıkmış Sorular Analizi"]}, {"week": 3, "topics": ["Nokta Atışı Bilgiler"]}, {"week": 4, "topics": ["Son Eksik Tamamlama"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Genel Tekrar"]}, {"week": 2, "topics": ["Motivasyon"]} ]}
        ],
        "Din Kültürü": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Kader İnancı"]}, {"week": 2, "topics": ["Zekat ve Sadaka"]}, {"week": 3, "topics": ["Din ve Hayat"]}, {"week": 4, "topics": ["Hz. Muhammed'in Örnekliği"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Kuran-ı Kerim ve Özellikleri"]}, {"week": 2, "topics": ["Ayetler ve Sureler"]}, {"week": 3, "topics": ["Hz. Yusuf Kıssası"]}, {"week": 4, "topics": ["Asr Suresi"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["İslam'ın Paylaşma ve Yardımlaşmaya Verdiği Önem"]}, {"week": 2, "topics": ["Zekat ve Sadaka İbadeti (Detay)"]}, {"week": 3, "topics": ["Maun Suresi"]}, {"week": 4, "topics": ["Din, Birey ve Toplum"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Dinin Temel Gayesi"]}, {"week": 2, "topics": ["Hz. Şuayb (a.s.)"]}, {"week": 3, "topics": ["Hz. Muhammed'in Doğruluğu"]}, {"week": 4, "topics": ["Hz. Muhammed'in Merhameti"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Hz. Muhammed'in Adaleti"]}, {"week": 2, "topics": ["Hz. Muhammed'in Cesareti"]}, {"week": 3, "topics": ["Hz. Muhammed'in İstişareye Önemi"]}, {"week": 4, "topics": ["Kureyş Suresi"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Kuran-ı Kerim'in Ana Konuları"]}, {"week": 2, "topics": ["İslam Dininin Korunması"]}, {"week": 3, "topics": ["Canın ve Malın Korunması"]}, {"week": 4, "topics": ["Aklın ve Neslin Korunması"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Hz. Nuh (a.s.)"]}, {"week": 2, "topics": ["Kadir Suresi"]}, {"week": 3, "topics": ["Ünite Tekrar: Kader"]}, {"week": 4, "topics": ["Ünite Tekrar: Zekat"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Ünite Tekrar: Din ve Hayat"]}, {"week": 2, "topics": ["Ünite Tekrar: Hz. Muhammed"]}, {"week": 3, "topics": ["Deneme Çözümü 1"]}, {"week": 4, "topics": ["Deneme Çözümü 2"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Kavram Çalışması"]}, {"week": 2, "topics": ["Ayet ve Hadis Yorumlama"]}, {"week": 3, "topics": ["Çıkmış Sorular"]}, {"week": 4, "topics": ["Son Tekrar"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Final Tekrarı"]}, {"week": 2, "topics": ["Motivasyon"]} ]}
        ],
        "Yabancı Dil": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Unit 1: Friendship"]}, {"week": 2, "topics": ["Accepting and Refusing"]}, {"week": 3, "topics": ["Unit 2: Teen Life"]}, {"week": 4, "topics": ["Regular Actions"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Unit 3: In The Kitchen"]}, {"week": 2, "topics": ["Process and Recipes"]}, {"week": 3, "topics": ["Unit 4: On The Phone"]}, {"week": 4, "topics": ["Phone Conversations"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Unit 5: The Internet"]}, {"week": 2, "topics": ["Internet Safety"]}, {"week": 3, "topics": ["Unit 6: Adventures"]}, {"week": 4, "topics": ["Extreme Sports"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Comparisons"]}, {"week": 2, "topics": ["Preferences"]}, {"week": 3, "topics": ["Unit 7: Tourism"]}, {"week": 4, "topics": ["Experiences"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Unit 8: Chores"]}, {"week": 2, "topics": ["Obligations"]}, {"week": 3, "topics": ["Unit 9: Science"]}, {"week": 4, "topics": ["Scientific Achievements"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Unit 10: Natural Forces"]}, {"week": 2, "topics": ["Predictions"]}, {"week": 3, "topics": ["Future Tense"]}, {"week": 4, "topics": ["General Revision: Units 1-5"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["General Revision: Units 6-10"]}, {"week": 2, "topics": ["Vocabulary Quiz"]}, {"week": 3, "topics": ["Reading Comprehension"]}, {"week": 4, "topics": ["Dialogue Completion"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["LGS Practice Exam 1"]}, {"week": 2, "topics": ["LGS Practice Exam 2"]}, {"week": 3, "topics": ["Important Vocabulary List"]}, {"week": 4, "topics": ["Common Expressions"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Last Look: Friendship & Teen Life"]}, {"week": 2, "topics": ["Last Look: Internet & Adventures"]}, {"week": 3, "topics": ["Last Look: Chores & Science"]}, {"week": 4, "topics": ["Mock Exam"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Final Revision"]}, {"week": 2, "topics": ["Exam Strategies"]} ]}
        ]
    }

    # UNIVERSAL POOLS for automatic gap-filling (ensures 7 topics per week)
    POOLS = {
        "Matematik": [
            "Temel \u0130\u015flem Yetene\u011fi", "Mant\u0131k Muhakeme Prati\u011fi", "Say\u0131sal Analiz \u00c7al\u0131\u015fmas\u0131",
            "LGS Tipi Soru Analizi", "H\u0131z Testi ve Zaman Y\u00f6netimi", "Hatal\u0131 Soru Analiz Teknikleri", "Genel Matematik Tekrar\u0131"
        ],
        "Fen Bilimleri": [
            "Bilimsel Muhakeme Becerisi", "Deney Analizi ve Yorumlama", "Yeni Nesil Soru \u00c7\u00f6z\u00fcm\u00fc",
            "Fen Bilimleri H\u0131z Testi", "Kavram Haritas\u0131 \u00c7al\u0131\u015fmas\u0131", "Laboratuvar Sorular\u0131 Analizi", "Fen Bilimleri Genel Tekrar"
        ],
        "T\u00fcrk\u00e7e": [
            "Paragraf H\u0131zland\u0131rma", "S\u00f6zel Mant\u0131k Becerisi", "Okuma Anlama ve Yorum",
            "S\u00f6zc\u00fckte Anlam Prati\u011fi", "Yaz\u0131m ve Noktalama Check", "Metin T\u00fcrleri Analizi", "T\u00fcrk\u00e7e Genel Tekrar"
        ],
        "T.C. \u0130nk\u0131lap Tarihi": [
            "Kronoloji Analiz Becerisi", "Harita ve G\u00f6rsel Yorumlama", "Kavram Bilgisi Tekrar\u0131",
            "Kaynak Analizi \u00c7al\u0131\u015fmas\u0131", "Tarihsel Muhakeme", "Olay-Olgu Ayr\u0131m\u0131", "\u0130nk\u0131lap Tarihi Genel Tekrar"
        ],
        "Yabanc\u0131 Dil": [
            "Vocabulary Builder (Focus)", "Reading Comprehension", "Grammar Review and Check",
            "Sentence Parsing Practice", "Word Association Games", "Translation Exercises", "English General Review"
        ],
        "Din K\u00fclt\u00fcr\u00fc": [
            "Metin Analizi ve Yorum", "Kavram Tekrar\u0131", "Ayet ve Hadis Yorumlama",
            "Ahlaki Tutum Analizi", "Dini Terimler S\u00f6zl\u00fc\u011f\u00fc", "Din K\u00fclt\u00fcr\u00fc Soru Prati\u011fi", "Din Bilgisi Genel Tekrar"
        ]
    }

    with transaction.atomic():
        total_count = 0
        all_new_topics = []
        
        # 1. Create/Identify Subjects
        subject_map = {}
        for subj_name in curr_data.keys():
            sub_obj, _ = Subject.objects.get_or_create(name=subj_name)
            subject_map[subj_name] = sub_obj

        # 2. Populate Standard Data + Fill Gaps with Pools (Target 7 per week)
        academic_months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        
        for subject_name, subject_obj in subject_map.items():
            pool = POOLS.get(subject_name, ["Genel Soru Prati\u011fi"])
            
            # Create month index for lookup
            month_data_map = {m["id"]: m["weeks"] for m in curr_data[subject_name]}
            
            for m_id in academic_months:
                weeks_list = month_data_map.get(m_id, [])
                # Convert week list to map for easier access
                week_to_topics = {w["week"]: w["topics"] for w in weeks_list}
                
                for w_id in range(1, 5):
                    # 1. Get primary topics
                    primary_topics = week_to_topics.get(w_id, [])
                    topic_titles = list(primary_topics)
                    
                    # 2. Fill gaps until we hit 7
                    pool_idx = 0
                    while len(topic_titles) < 7:
                        fill_title = pool[pool_idx % len(pool)]
                        if fill_title not in topic_titles:
                            topic_titles.append(fill_title)
                        pool_idx += 1
                        if pool_idx > 50: break # Safety
                    
                    # 3. Create objects
                    for idx, title in enumerate(topic_titles):
                        all_new_topics.append(Topic(
                            subject=subject_obj,
                            month=m_id,
                            week=w_id,
                            order=idx,
                            title=title
                        ))
                        total_count += 1
        
        # 3. Clear and Bulk Create
        if not Topic.objects.exists():
            Topic.objects.bulk_create(all_new_topics)
            log(f"Synced {total_count} curriculum topics via HIGH-DENSITY BULK CREATE.")
        else:
             log("Topics already exist. Skipping bulk create.")

        # 4. Student Config Fix
        students = Student.objects.all()
        for student in students:
            config, _ = CoachingConfig.objects.get_or_create(student=student)
            if not config.current_academic_month:
                config.current_academic_month = 2 # February
                config.current_academic_week = 3 # End of Feb
                config.save()
                log(f"Student {student.id} config initialized.")

    log("--- RESCUE ENGINE COMPLETED ---")
    return True

def run_nuclear_wipe(stdout=None):
    """
    Completely wipes the database and rebuilds it.
    The ultimate "Start Over" button.
    """
    from coaching.models import Subject, Topic, StudentProgress
    from students.models import StudyTask
    from django.db import transaction

    def log(msg):
        if stdout:
            stdout.write(msg)
        print(msg)

    log("!!! NUCLEAR WIPE INITIATED !!!")
    
    # Use atomic to ensure we don't get partial states
    with transaction.atomic():
        log("1. Deleting Student Progress & Tasks...")
        # Delete dependent objects first
        StudyTask.objects.all().delete()
        StudentProgress.objects.all().delete()
        
        log("2. Deleting Topics...")
        # Delete topics. This cascades to progress if any missed.
        # We use .all().delete() which is efficient enough for 2000 items.
        count, _ = Topic.objects.all().delete()
        log(f"Deleted {count} topics.")
        
        log("3. Deleting Subjects...")
        # Only delete subjects if we really want to purge everything.
        # Actually, keeping subjects is fine, but let's be thorough.
        Subject.objects.all().delete()
        
        log("4. Rebuilding from scratch (V2)...")
        # Now rebuild without checking for existence because we JUST wiped it.
        # Run logic with 'force=True' implied by the empty state.
        run_rescue_logic(stdout=stdout)
    
    log("!!! NUCLEAR WIPE COMPLETED SUCCESSFULLY !!!")
    return True
