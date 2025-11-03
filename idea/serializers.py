from rest_framework import serializers
from .models import *

class TaskAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True)  # ⚠️ Сделали необязательным

    def to_internal_value(self, data):
        # Если data уже является словарем (из JSON), возвращаем как есть
        if isinstance(data, dict):
            return data
        # Если это объект файла (из multipart), обрабатываем соответствующим образом
        return super().to_internal_value(data)

    class Meta:
        model = TaskAttachment
        fields = ['id', 'name', 'file', 'link']


class TaskNoteSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, allow_blank=True)  # ⚠️ Сделали необязательным
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = TaskNote
        fields = ['id', 'text', 'author', 'author_name', 'created_at']
        read_only_fields = ['author', 'created_at', 'author_name']


class TaskSerializer(serializers.ModelSerializer):
    attachments = TaskAttachmentSerializer(many=True, required=False)
    notes = TaskNoteSerializer(many=True, required=False)

    is_completed = serializers.BooleanField(default=False)
    has_question = serializers.BooleanField(default=False)
    is_urgent = serializers.BooleanField(default=False)
    is_planned = serializers.BooleanField(default=False)
    is_think = serializers.BooleanField(default=False)
    is_hidden = serializers.BooleanField(default=False)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_at_text', 'deadline_text',
            'is_completed', 'has_question', 'is_urgent', 'is_planned',
            'is_think', 'is_hidden', 'created_at', 'attachments', 'notes'
        ]

    def create(self, validated_data):
        # Берем данные из контекста, а не из validated_data
        request_data = self.context.get('request_data', {})

        attachments_data = request_data.get('attachments', [])
        notes_data = request_data.get('notes', [])

        print("=== CREATE TASK ===")
        print("Validated data:", validated_data)
        print("Attachments data:", attachments_data)
        print("Notes data:", notes_data)

        # Создаем задачу
        task = Task.objects.create(**validated_data)

        # Создаем вложения
        for att_data in attachments_data:
            if isinstance(att_data, dict):
                # Обрабатываем пустой файл
                file_obj = att_data.get('file')
                if file_obj == {}:
                    file_obj = None

                TaskAttachment.objects.create(
                    task=task,
                    name=att_data.get('name', ''),
                    link=att_data.get('link', ''),
                    file=file_obj
                )

        # Создаем заметки
        for note_data in notes_data:
            if isinstance(note_data, dict):
                TaskNote.objects.create(
                    task=task,
                    author=self.context['request'].user,
                    text=note_data.get('text', '')
                )

        return task

    def update(self, instance, validated_data):
        print("Validated data:", validated_data)

        # Получаем исходные данные из контекста
        request_data = self.context.get('request_data', {})
        print("Request data:", request_data)

        attachments_data = request_data.get('attachments', [])
        notes_data = request_data.get('notes', [])
        print("Attachments data:", attachments_data)
        print("Notes data:", notes_data)

        # Обновляем основные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обрабатываем вложения
        self._handle_attachments(instance, attachments_data)

        # Обрабатываем заметки
        self._handle_notes(instance, notes_data)

        return instance

    def _handle_attachments(self, instance, attachments_data):
        """Обработка вложений с правильной работой с файлами"""
        if not attachments_data:
            return

        existing_attachments = {att.id: att for att in instance.attachments.all()}
        received_ids = set()

        for att_data in attachments_data:
            if not isinstance(att_data, dict):
                continue

            att_id = att_data.get('id')
            name = att_data.get('name', '')
            link = att_data.get('link', '')
            file_obj = att_data.get('file')

            print(f"Processing attachment - ID: {att_id}, Name: {name}, File: {file_obj}")

            if att_id and att_id in existing_attachments:
                # Обновляем существующее вложение
                attachment = existing_attachments[att_id]
                attachment.name = name
                attachment.link = link

                # Обновляем файл только если передан новый файл
                if file_obj and hasattr(file_obj, 'file'):  # Проверяем, что это реальный файл
                    attachment.file = file_obj
                    print(f"Updated file for attachment {att_id}")

                attachment.save()
                received_ids.add(att_id)
            else:
                # Создаем новое вложение
                new_attachment = TaskAttachment.objects.create(
                    task=instance,
                    name=name,
                    link=link,
                    file=file_obj if file_obj and hasattr(file_obj, 'file') else None
                )
                print(f"Created new attachment with ID: {new_attachment.id}")

        # Удаляем вложения, которых нет в полученных данных
        for att_id, attachment in existing_attachments.items():
            if att_id not in received_ids:
                print(f"Deleting attachment {att_id}")
                attachment.delete()

    def _handle_notes(self, instance, notes_data):
        """Обработка заметок: обновление, создание, удаление"""
        if notes_data is None:
            return

        existing_notes = {note.id: note for note in instance.notes.all()}
        received_ids = set()

        for note_data in notes_data:
            note_id = note_data.get('id')

            if note_id and note_id in existing_notes:
                # Обновляем существующую заметку
                note = existing_notes[note_id]
                for key, value in note_data.items():
                    if key not in ['id', 'author']:  # Не обновляем ID и автора
                        setattr(note, key, value)
                note.save()
                received_ids.add(note_id)
            else:
                # Создаем новую заметку
                TaskNote.objects.create(
                    task=instance,
                    author=self.context['request'].user,
                    **note_data
                )

        # Удаляем заметки, которых нет в полученных данных
        for note_id, note in existing_notes.items():
            if note_id not in received_ids:
                note.delete()


class ReelsExampleLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelsExampleLink
        fields = ['id', 'name', 'link']

class ReelsIdeaSerializer(serializers.ModelSerializer):
    example_links = ReelsExampleLinkSerializer(many=True, required=False)

    class Meta:
        model = ReelsIdea
        fields = [
            'id', 'reels_number', 'title', 'plot_description',
            'created_at', 'is_approved', 'admin_comment', 'example_links'
        ]

    def create(self, validated_data):
        # Берем данные из контекста
        request_data = self.context.get('request_data', {})
        links_data = request_data.get('example_links', [])

        print("=== CREATE REELS IDEA ===")
        print("Validated data:", validated_data)
        print("Links data:", links_data)

        # Создаем основную идею
        idea = ReelsIdea.objects.create(**validated_data)

        # Создаем ссылки
        for link_data in links_data:
            if isinstance(link_data, dict):
                ReelsExampleLink.objects.create(
                    reels_idea=idea,
                    name=link_data.get('name', ''),
                    link=link_data.get('link', '')
                )

        return idea

    def update(self, instance, validated_data):
        print("Validated data:", validated_data)

        # Берем данные из контекста, а не из validated_data
        request_data = self.context.get('request_data', {})
        links_data = request_data.get('example_links', [])

        print("Request data example_links:", links_data)

        # Обновляем основные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем ссылки
        instance.example_links.all().delete()
        for link_data in links_data:
            if isinstance(link_data, dict):
                ReelsExampleLink.objects.create(
                    reels_idea=instance,
                    name=link_data.get('name', ''),
                    link=link_data.get('link', '')
                )

        return instance







class MasterClassMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClassMaterial
        fields = "__all__"


class MasterClassExampleLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClassExampleLink
        fields = "__all__"


class MasterClassFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClassFile
        fields = "__all__"


class MasterClassDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClassDate
        fields = "__all__"


class MasterClassIdeaSerializer(serializers.ModelSerializer):
    materials = MasterClassMaterialSerializer(many=True, read_only=True)
    example_links = MasterClassExampleLinkSerializer(many=True, read_only=True)
    files = MasterClassFileSerializer(many=True, read_only=True)
    dates = MasterClassDateSerializer(many=True, read_only=True)

    class Meta:
        model = MasterClassIdea
        fields = "__all__"
        extra_kwargs = {
            'cover': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        # Получаем данные из контекста
        request_data = self.context.get('request_data', {})

        materials_data = request_data.get('materials', [])
        example_links_data = request_data.get('example_links', [])
        dates_data = request_data.get('dates', [])
        files_data = request_data.get('files', [])

        # Создаем основную запись
        mk_idea = MasterClassIdea.objects.create(**validated_data)

        # Создаем материалы
        for material_data in materials_data:
            if isinstance(material_data, dict):
                MasterClassMaterial.objects.create(
                    mk_idea=mk_idea,
                    name=material_data.get('name', ''),
                    comment=material_data.get('comment', ''),
                    source_link=material_data.get('source_link', ''),
                    received_date_text=material_data.get('received_date_text', ''),
                    cost_text=material_data.get('cost_text', '')
                )

        # Создаем примеры ссылок
        for link_data in example_links_data:
            if isinstance(link_data, dict):
                MasterClassExampleLink.objects.create(
                    mk_idea=mk_idea,
                    name=link_data.get('name', ''),
                    link=link_data.get('link', '')
                )

        # Создаем даты
        for date_data in dates_data:
            if isinstance(date_data, dict):
                MasterClassDate.objects.create(
                    mk_idea=mk_idea,
                    date_text=date_data.get('date_text', '')
                )

        # Создаем файлы
        for file_data in files_data:
            if isinstance(file_data, dict):
                MasterClassFile.objects.create(
                    mk_idea=mk_idea,
                    name=file_data.get('name', ''),
                    file=file_data.get('file')
                )

        return mk_idea

    def update(self, instance, validated_data):
        request_data = self.context.get('request_data', {})

        materials_data = request_data.get('materials', [])
        example_links_data = request_data.get('example_links', [])
        dates_data = request_data.get('dates', [])
        files_data = request_data.get('files', [])

        # Обновляем основные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обрабатываем материалы
        self._handle_materials(instance, materials_data)

        # Обрабатываем примеры ссылок
        self._handle_example_links(instance, example_links_data)

        # Обрабатываем даты
        self._handle_dates(instance, dates_data)

        # Обрабатываем файлы
        self._handle_files(instance, files_data)

        return instance

    def _handle_materials(self, instance, materials_data):
        """Обработка материалов"""
        existing_materials = {mat.id: mat for mat in instance.materials.all()}
        received_ids = set()

        for material_data in materials_data:
            if not isinstance(material_data, dict):
                continue

            material_id = material_data.get('id')

            if material_id and material_id in existing_materials:
                # Обновляем существующий материал
                material = existing_materials[material_id]
                material.name = material_data.get('name', '')
                material.comment = material_data.get('comment', '')
                material.source_link = material_data.get('source_link', '')
                material.received_date_text = material_data.get('received_date_text', '')
                material.cost_text = material_data.get('cost_text', '')
                material.save()
                received_ids.add(material_id)
            else:
                # Создаем новый материал
                MasterClassMaterial.objects.create(
                    mk_idea=instance,
                    name=material_data.get('name', ''),
                    comment=material_data.get('comment', ''),
                    source_link=material_data.get('source_link', ''),
                    received_date_text=material_data.get('received_date_text', ''),
                    cost_text=material_data.get('cost_text', '')
                )

        # Удаляем материалы, которых нет в полученных данных
        for material_id, material in existing_materials.items():
            if material_id not in received_ids:
                material.delete()

    def _handle_example_links(self, instance, example_links_data):
        """Обработка примеров ссылок"""
        existing_links = {link.id: link for link in instance.example_links.all()}
        received_ids = set()

        for link_data in example_links_data:
            if not isinstance(link_data, dict):
                continue

            link_id = link_data.get('id')

            if link_id and link_id in existing_links:
                # Обновляем существующую ссылку
                link = existing_links[link_id]
                link.name = link_data.get('name', '')
                link.link = link_data.get('link', '')
                link.save()
                received_ids.add(link_id)
            else:
                # Создаем новую ссылку
                MasterClassExampleLink.objects.create(
                    mk_idea=instance,
                    name=link_data.get('name', ''),
                    link=link_data.get('link', '')
                )

        # Удаляем ссылки, которых нет в полученных данных
        for link_id, link in existing_links.items():
            if link_id not in received_ids:
                link.delete()

    def _handle_dates(self, instance, dates_data):
        """Обработка дат"""
        existing_dates = {date.id: date for date in instance.dates.all()}
        received_ids = set()

        for date_data in dates_data:
            if not isinstance(date_data, dict):
                continue

            date_id = date_data.get('id')

            if date_id and date_id in existing_dates:
                # Обновляем существующую дату
                date = existing_dates[date_id]
                date.date_text = date_data.get('date_text', '')
                date.save()
                received_ids.add(date_id)
            else:
                # Создаем новую дату
                MasterClassDate.objects.create(
                    mk_idea=instance,
                    date_text=date_data.get('date_text', '')
                )

        # Удаляем даты, которых нет в полученных данных
        for date_id, date in existing_dates.items():
            if date_id not in received_ids:
                date.delete()

    def _handle_files(self, instance, files_data):
        """Обработка файлов"""
        # Для файлов просто удаляем старые и создаем новые
        # (так как обновление файлов сложнее)
        #instance.files.all().delete()
        print(files_data)
        for file_data in files_data:
            if isinstance(file_data, dict):
                MasterClassFile.objects.create(
                    mk_idea=instance,
                    name=file_data.get('name', ''),
                    file=file_data.get('file')
                )