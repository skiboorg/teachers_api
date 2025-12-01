from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class Task(models.Model):
    """
    Задачи — список дел и планов.
    """

    title = models.CharField("Название задачи", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    created_at_text = models.CharField("Дата постановки (текст)", max_length=255, blank=True, null=True)
    deadline_text = models.CharField("Дедлайн (текст)", max_length=255, blank=True, null=True)
    is_completed = models.BooleanField("Выполнена", default=False)
    has_question = models.BooleanField("Есть вопрос", default=False)
    is_urgent = models.BooleanField("Срочная", default=False)
    is_planned = models.BooleanField("Плановая", default=False)
    is_think = models.BooleanField("Подумать", default=False)
    is_hidden = models.BooleanField("Скрыть задачу (только админ видит)", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TaskAttachment(models.Model):
    """
    Прикреплённые файлы или ссылки к задаче.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    name = models.CharField("Название", max_length=255)
    file = models.FileField("Файл", upload_to="task_files/", blank=True, null=True)
    link = models.TextField("Ссылка", blank=True, null=True)

    class Meta:
        verbose_name = "Прикрепление"
        verbose_name_plural = "Прикрепления"


class TaskNote(models.Model):
    """
    Пометки к задаче (как комментарии).
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    text = models.TextField("Текст пометки")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Пометка"
        verbose_name_plural = "Пометки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Пометка от {self.author} ({self.created_at.date()})"

class ReelsTag(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        verbose_name = "Тег рилсов"
        verbose_name_plural = "Теги рилсов"

    def __str__(self):
        return f"{self.name}"

class ReelsIdea(models.Model):
    """
    Идея для Reels.
    """
    author = models.CharField(max_length=50,blank=True, null=True)
    tags =  models.ManyToManyField(ReelsTag,blank=True)
    reels_number = models.CharField("Номер Reels", max_length=50,blank=True, null=True)
    title = models.CharField("Название", max_length=255,blank=True, null=True)
    plot_description = models.TextField("Описание сюжета",blank=True, null=True)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    is_approved = models.BooleanField("Одобрено", default=False,blank=True, null=True)
    admin_comment = models.TextField("Комментарий администратора", blank=True, null=True)

    class Meta:
        verbose_name = "Идея для Reels"
        verbose_name_plural = "Идеи для Reels"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reels_number} — {self.title}"


class ReelsExampleLink(models.Model):
    """
    Ссылки на примеры Reels.
    """

    reels_idea = models.ForeignKey(ReelsIdea, on_delete=models.CASCADE, related_name="example_links")
    name = models.CharField("Название", max_length=255)
    link = models.TextField("Ссылка")

    class Meta:
        verbose_name = "Ссылка на пример Reels"
        verbose_name_plural = "Ссылки на примеры Reels"


class MasterClassTag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Тег МК"
        verbose_name_plural = "Теги МК"

    def __str__(self):
        return f"{self.name}"



class MasterClassIdea(models.Model):
    """
    Идея для мастер-класса.
    """
    tags = models.ManyToManyField(MasterClassTag, blank=True)
    mk_number = models.CharField("Номер МК", max_length=50,blank=True, null=True)
    title = models.CharField("Название", max_length=255,blank=True, null=True)
    cover = models.ImageField("Обложка (500x300)", upload_to="mk_covers/",blank=True, null=True)
    description = CKEditor5Field("Описание МК (HTML)", blank=True, null=True)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    is_approved = models.BooleanField("Одобрено", default=False)
    admin_comment = models.TextField("Комментарий администратора", blank=True, null=True)

    class Meta:
        verbose_name = "Идея для МК"
        verbose_name_plural = "Идеи для МК"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.mk_number} — {self.title}"


class MasterClassMaterial(models.Model):
    """
    Материалы для мастер-класса.
    """

    mk_idea = models.ForeignKey(MasterClassIdea, on_delete=models.CASCADE, related_name="materials")
    name = models.CharField("Название", max_length=255)
    comment = models.TextField("Комментарий", blank=True, null=True)
    source_link = models.TextField("Где взять (ссылка)", blank=True, null=True)
    received_date_text = models.CharField("Дата получения материалов", max_length=255, blank=True, null=True)
    cost_text = models.CharField("Стоимость", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Материал для МК"
        verbose_name_plural = "Материалы для МК"


class MasterClassExampleLink(models.Model):
    """
    Ссылки на примеры для МК.
    """

    mk_idea = models.ForeignKey(MasterClassIdea, on_delete=models.CASCADE, related_name="example_links")
    name = models.CharField("Название", max_length=255)
    link = models.TextField("Ссылка")

    class Meta:
        verbose_name = "Ссылка на пример МК"
        verbose_name_plural = "Ссылки на примеры МК"


class MasterClassFile(models.Model):
    """
    Файлы для мастер-класса.
    """

    mk_idea = models.ForeignKey(MasterClassIdea, on_delete=models.CASCADE, related_name="files")
    name = models.CharField("Название", max_length=255)
    file = models.FileField("Файл", upload_to="mk_files/")

    class Meta:
        verbose_name = "Файл МК"
        verbose_name_plural = "Файлы МК"


class MasterClassDate(models.Model):
    """
    Даты проведения мастер-класса.
    """

    mk_idea = models.ForeignKey(MasterClassIdea, on_delete=models.CASCADE, related_name="dates")
    date_text = models.CharField("Дата проведения (текст)", max_length=255)

    class Meta:
        verbose_name = "Дата МК"
        verbose_name_plural = "Даты МК"
