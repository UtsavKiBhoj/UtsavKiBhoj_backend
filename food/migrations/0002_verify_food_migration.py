from django.db import migrations, models

def forwards(apps, schema_editor):
    Event = apps.get_model('events', 'Event')  # Explicitly get the model
    FoodDetail = apps.get_model('food', 'FoodDetail')
    schema_editor.add_field(
        FoodDetail,
        models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='food_details')
    )

class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
