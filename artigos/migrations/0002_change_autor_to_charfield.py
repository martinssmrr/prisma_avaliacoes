# Generated manually to migrate autor field from ForeignKey to CharField

from django.db import migrations, models


def migrate_autor_data(apps, schema_editor):
    """
    Converte os dados do campo autor de ForeignKey para CharField
    """
    Artigo = apps.get_model('artigos', 'Artigo')
    User = apps.get_model('auth', 'User')
    
    for artigo in Artigo.objects.all():
        if hasattr(artigo, 'autor_old') and artigo.autor_old:
            try:
                user = User.objects.get(id=artigo.autor_old.id)
                # Pega o nome completo ou username do usuário
                autor_name = user.get_full_name() or user.username
                artigo.autor_new = autor_name
                artigo.save()
            except (User.DoesNotExist, AttributeError):
                artigo.autor_new = "Autor Desconhecido"
                artigo.save()
        elif not hasattr(artigo, 'autor_new') or not artigo.autor_new:
            artigo.autor_new = "Equipe Prisma"
            artigo.save()


def reverse_migrate_autor_data(apps, schema_editor):
    """
    Operação reversa (não implementada pois perderia dados)
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('artigos', '0001_initial'),
    ]

    operations = [
        # Passo 1: Adicionar o novo campo CharField
        migrations.AddField(
            model_name='artigo',
            name='autor_new',
            field=models.CharField(
                max_length=100,
                verbose_name="Autor",
                help_text="Nome do autor do artigo",
                null=True,
                blank=True
            ),
        ),
        
        # Passo 2: Renomear o campo antigo
        migrations.RenameField(
            model_name='artigo',
            old_name='autor',
            new_name='autor_old',
        ),
        
        # Passo 3: Migrar os dados
        migrations.RunPython(migrate_autor_data, reverse_migrate_autor_data),
        
        # Passo 4: Remover o campo antigo
        migrations.RemoveField(
            model_name='artigo',
            name='autor_old',
        ),
        
        # Passo 5: Renomear o novo campo para o nome correto
        migrations.RenameField(
            model_name='artigo',
            old_name='autor_new',
            new_name='autor',
        ),
        
        # Passo 6: Remover null=True do campo final
        migrations.AlterField(
            model_name='artigo',
            name='autor',
            field=models.CharField(
                max_length=100,
                verbose_name="Autor",
                help_text="Nome do autor do artigo"
            ),
        ),
    ]
