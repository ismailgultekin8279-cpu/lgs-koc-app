from django.core.management.base import BaseCommand
from coaching.models import Subject, Topic, CoachingConfig
from students.models import Student
from coaching.services import CoachingService
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates LGS curriculum and activates student configurations for live deployment.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- STARTING LIVE RESCUE ORCHESTRATION ---'))

        # 1. Ensure Subjects
        subjects_data = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Din Kültürü", "Yabancı Dil"]
        for name in subjects_data:
            slug = slugify(name.replace('ı', 'i').replace('İ', 'I'))
            obj, created = Subject.objects.get_or_create(name=name, defaults={"slug": slug})
            if created:
                self.stdout.write(f"Subject Created: {name}")

        # 2. Populate Curriculum (Idempotent)
        POOLS = {
            "Matematik": ["Temel İşlem Yeteneği", "Mantık Muhakeme Pratiği", "Sayısal Analiz Çalışması", "LGS Tipi Soru Analizi", "Hız Testi ve Zaman Yönetimi", "Hatalı Soru Analiz Teknikleri", "Genel Matematik Tekrarı"],
            "Fen Bilimleri": ["Bilimsel Muhakeme Becerisi", "Deney Analizi ve Yorumlama", "Yeni Nesil Soru Çözümü", "Fen Bilimleri Hız Testi", "Kavram Haritası Çalışması", "Laboratuvar Soruları Analizi", "Fen Bilimleri Genel Tekrar"],
            "Türkçe": ["Paragraf Hızlandırma", "Sözel Mantık Becerisi", "Okuma Anlama ve Yorum", "Sözcükte Anlam Pratiği", "Yazım ve Noktalama Check", "Metin Türleri Analizi", "Türkçe Genel Tekrar"],
            "T.C. İnkılap Tarihi": ["Kronoloji Analiz Becerisi", "Harita ve Görsel Yorumlama", "Kavram Bilgisi Tekrarı", "Kaynak Analizi Çalışması", "Tarihsel Muhakeme", "Olay-Olgu Ayrımı", "İnkılap Tarihi Genel Tekrar"],
            "Yabancı Dil": ["Vocabulary Builder (Focus)", "Reading Comprehension", "Grammar Review and Check", "Sentence Parsing Practice", "Word Association Games", "Translation Exercises", "English General Review"],
            "Din Kültürü": ["Metin Analizi ve Yorum", "Kavram Tekrarı", "Ayet ve Hadis Yorumlama", "Ahlaki Tutum Analizi", "Dini Terimler Sözlüğü", "Din Kültürü Soru Pratiği", "Din Bilgisi Genel Tekrar"]
        }
        
        months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        total_topics = 0
        for subj_name, pool in POOLS.items():
            sub = Subject.objects.get(name=subj_name)
            for m in months:
                for w in range(1, 5):
                    existing = Topic.objects.filter(subject=sub, month=m, week=w).count()
                    if existing < 7:
                        needed = 7 - existing
                        for i in range(needed):
                            Topic.objects.create(
                                subject=sub, month=m, week=w,
                                order=existing + i,
                                title=pool[(existing + i) % len(pool)]
                            )
                            total_topics += 1
        self.stdout.write(self.style.SUCCESS(f"Populated {total_topics} topics across the curriculum."))

        # 3. Activate Students
        students = Student.objects.all()
        for student in students:
            config, created = CoachingConfig.objects.get_or_create(student=student)
            if created or not config.current_academic_month:
                config.current_academic_month = 9
                config.current_academic_week = 1
                config.target_score = 300
                config.save()
                self.stdout.write(f"Config Activated for: {student.full_name}")
            
            # 4. Generate Initial Plan if empty
            if not student.study_tasks.exists():
                service = CoachingService(student)
                service.generate_daily_plan()
                self.stdout.write(f"Initial Plan Generated for: {student.full_name}")

        self.stdout.write(self.style.SUCCESS('--- LIVE RESCUE COMPLETE ---'))
