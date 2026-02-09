from django.core.management.base import BaseCommand
from coaching.models import Subject, Topic, CoachingConfig, StudentProgress
from students.models import Student, StudyTask
from coaching.rescue_engine import run_rescue_logic
from django.db import transaction

class Command(BaseCommand):
    help = 'Wipes the existing curriculum and student tasks for a completely fresh start.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("!!! WARNING: NUCLEAR WIPE INITIATED !!!"))
        
        with transaction.atomic():
            # 1. Clear everything
            self.stdout.write("Wiping Study Tasks and Student Progress...")
            StudyTask.objects.all().delete()
            StudentProgress.objects.all().delete()
            
            self.stdout.write("Wiping Curriculum (Topics and Subjects)...")
            Topic.objects.all().delete()
            Subject.objects.all().delete()
            
            self.stdout.write("Clearing Student Coaching Configurations...")
            CoachingConfig.objects.all().update(current_academic_month=None, current_academic_week=None)

            self.stdout.write(self.style.SUCCESS("Cleanup complete. Database is now empty."))

            # 2. Run Rescue with the Full Curriculum (1680 Topics)
            self.stdout.write("Initializing Full 10-Month LGS Curriculum...")
            run_rescue_logic(stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS("--- FRESH START COMPLETED SUCCESSFULLY ---"))
        self.stdout.write(self.style.SUCCESS("You can now refresh the app and enjoy the full experience!"))
