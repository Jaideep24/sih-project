from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('sih_app', '0002_rename_entry_journalentry_entry_text_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]
