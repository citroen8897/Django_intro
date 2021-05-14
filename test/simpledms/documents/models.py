from django.db import models


class Document(models.Model):
    title = models.CharField(verbose_name="Назва", max_length=100, default='-', db_index=True)
    main_file = models.FileField(verbose_name="Головинй файл", upload_to='document/', null=True,
                                 max_length=500)
    reg_number = models.CharField(verbose_name="Реєстраціний номер", max_length=100, null=True, db_index=True)
    create_date = models.DateField(verbose_name="Дата створення документа", auto_now_add=True, editable=False,
                                   db_index=True, null=True)
    comment = models.TextField(verbose_name="Короткий зміст", max_length=500, null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'

    def __str__(self):
        return f'Документ №{self.reg_number or ""} від  {self.create_date}'
