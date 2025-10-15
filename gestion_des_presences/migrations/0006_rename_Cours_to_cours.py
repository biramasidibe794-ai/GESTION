from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_des_presences', '0005_rename_anneer_etudiant_annee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presence',
            old_name='Cours',
            new_name='cours',
        ),
    ]
