from coaching.models import Subject, Topic, CoachingConfig
from students.models import Student
from django.utils.text import slugify
from django.db import transaction

def run_rescue_logic(stdout=None):
    """
    Core rescue logic to populate the database and fix student configurations.
    """
    def log(msg):
        if stdout:
            stdout.write(msg)
        print(msg)

    log("--- STARTING RESCUE ENGINE (DIRECT CALL) ---")
    
    with transaction.atomic():
        # 1. Ensure Subjects
        # We use a mapping to handle Turkish characters safely
        subjects_map = {
            "Matematik": "matematik",
            "Fen Bilimleri": "fen-bilimleri",
            "Turkce": "turkce",
            "T.C. Inkilap Tarihi": "inkilap-tarihi",
            "Din Kulturu": "din-kulturu",
            "Yabanci Dil": "yabanci-dil"
        }
        
        # Mapping back to Turkish for display
        display_names = {
            "Turkce": "Türkçe",
            "Inkilap": "T.C. İnkılap Tarihi",
            "Din": "Din Kültürü"
        }

        for name, slug in subjects_map.items():
            disp_name = display_names.get(name, name)
            Subject.objects.get_or_create(slug=slug, defaults={"name": disp_name})

        # 2. Populate Curriculum (Minimal set for LGS)
        POOLS = {
            "matematik": ["Üslü İfadeler", "Kareköklü İfadeler", "Veri Analizi", "Olasılık", "Cebirsel İfadeler"],
            "fen-bilimleri": ["Mevsimler ve İklim", "DNA ve Genetik Kod", "Basınç", "Madde ve Endüstri"],
            "turkce": ["Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam", "Yazım Kuralları"],
            "inkilap-tarihi": ["Bir Kahraman Doğuyor", "Milli Uyanış", "Milli Bir Destan"],
            "din-kulturu": ["Kader İnancı", "Zekat ve Sadaka", "Din ve Hayat"],
            "yabanci-dil": ["Friendship", "Teen Life", "In The Kitchen"]
        }
        
        months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        total_topics = 0
        for slug, pool in POOLS.items():
            sub = Subject.objects.get(slug=slug)
            for m in months:
                for w in range(1, 5):
                    existing = Topic.objects.filter(subject=sub, month=m, week=w).count()
                    if existing < 3:
                        for i in range(3 - existing):
                            Topic.objects.create(
                                subject=sub, month=m, week=w,
                                order=existing + i,
                                title=pool[(existing + i) % len(pool)]
                            )
                            total_topics += 1
        log(f"Synced {total_topics} curriculum topics.")

        # 3. Student Config Fix
        students = Student.objects.all()
        for student in students:
            config, _ = CoachingConfig.objects.get_or_create(student=student)
            config.current_academic_month = 2 # February
            config.current_academic_week = 2
            config.save()
            log(f"Student {student.id} config synchronized for February.")

    log("--- RESCUE ENGINE COMPLETED ---")
    return True
