from rest_framework import viewsets, permissions, generics
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class ReelsTagListView(generics.ListAPIView):
    serializer_class = ReelsTagSerializer
    queryset = ReelsTag.objects.all()

class MKTagListView(generics.ListAPIView):
    serializer_class = MasterClassTagSerializer
    queryset = MasterClassTag.objects.all()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    arser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def _link_files_to_attachments(self, attachments_data, files):
        """Связывает файлы с вложениями по ID или индексу"""
        if not attachments_data or not files:
            return attachments_data

        # Собираем все файлы
        file_mapping = {}
        for key, file_obj in files.items():
            # Обрабатываем file_0, file_1, attachments[0][file] и т.д.
            if key.startswith('file_'):
                # file_0, file_1, file_2
                try:
                    index = int(key.split('_')[1])
                    file_mapping[f'index_{index}'] = file_obj
                except (IndexError, ValueError):
                    pass
            elif 'attachments' in key and 'file' in key:
                # attachments[0][file], attachments[1][file]
                try:
                    index = int(key.split('[')[1].split(']')[0])
                    file_mapping[f'index_{index}'] = file_obj
                except (IndexError, ValueError):
                    pass

        print("File mapping:", file_mapping)

        # Связываем файлы с вложениями
        for i, attachment in enumerate(attachments_data):
            if isinstance(attachment, dict):
                file_key = f'index_{i}'
                if file_key in file_mapping:
                    attachment['file'] = file_mapping[file_key]
                    print(f"Linked file to attachment index {i}")
                else:
                    attachment['file'] = None

        return attachments_data


    def get_serializer_context(self):
        import json
        context = super().get_serializer_context()

        if self.request.method in ['POST', 'PUT', 'PATCH']:
            data = self.request.data.copy()

            print("=== RAW REQUEST DATA ===")
            print("Data:", dict(data))
            print("Files:", dict(self.request.FILES))

            # Обрабатываем attachments
            if 'attachments' in data:
                attachments_data = []

                if isinstance(data['attachments'], str):
                    try:
                        attachments_data = json.loads(data['attachments'])
                    except json.JSONDecodeError:
                        attachments_data = []
                elif isinstance(data['attachments'], list):
                    attachments_data = data['attachments']

                # Связываем файлы с вложениями
                attachments_data = self._link_files_to_attachments(attachments_data, self.request.FILES)

                data['attachments'] = attachments_data

            # Обрабатываем notes
            if 'notes' in data and isinstance(data['notes'], str):
                try:
                    data['notes'] = json.loads(data['notes'])
                except json.JSONDecodeError:
                    data['notes'] = []

            print("=== PROCESSED DATA ===")
            print("Attachments:", data.get('attachments'))

            context['request_data'] = data

        return context
    def get_queryset(self):
        user = self.request.user
        # # Если нужно скрывать задачи с is_hidden для не-админов
        # if user.is_staff:
        #     return Task.objects.all()
        return Task.objects.filter(is_hidden=False)


class ReelsIdeaViewSet(viewsets.ModelViewSet):
    queryset = ReelsIdea.objects.all()
    serializer_class = ReelsIdeaSerializer
    # permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        queryset = super().get_queryset()
        tag_name = self.request.query_params.get('tag_id', None)

        if tag_name:
            # Фильтруем по тегу (регистронезависимо)
            queryset = queryset.filter(tags__id=tag_name)

        return queryset.distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.request.method in ['POST', 'PUT', 'PATCH']:
            data = self.request.data.copy()

            # Обрабатываем example_links для всех методов
            if 'example_links' in data:
                if isinstance(data['example_links'], str):
                    import json
                    try:
                        data['example_links'] = json.loads(data['example_links'])
                    except json.JSONDecodeError:
                        data['example_links'] = []
                elif data['example_links'] is None:
                    # Если example_links = None, устанавливаем пустой список
                    data['example_links'] = []
            else:
                # Если поля example_links нет вообще, устанавливаем пустой список
                data['example_links'] = []

            print("=== PROCESSED DATA ===")
            print("Method:", self.request.method)
            print("example_links:", data.get('example_links'))

            context['request_data'] = data

        return context


class MasterClassIdeaViewSet(viewsets.ModelViewSet):
    queryset = MasterClassIdea.objects.all()
    serializer_class = MasterClassIdeaSerializer
    # permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        queryset = super().get_queryset()
        tag_name = self.request.query_params.get('tag_id', None)

        if tag_name:
            # Фильтруем по тегу (регистронезависимо)
            queryset = queryset.filter(tags__id=tag_name)

        return queryset.distinct()
    def get_serializer_context(self):
        import json
        context = super().get_serializer_context()

        if self.request.method in ['POST', 'PUT', 'PATCH']:
            data = self.request.data.copy()

            # Обрабатываем nested данные из FormData
            for field in ['materials', 'example_links', 'dates']:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except json.JSONDecodeError:
                        data[field] = []

            # Обрабатываем файлы
            files_data = []
            i = 0
            while f'files[{i}][file]' in self.request.FILES:
                file_obj = self.request.FILES.get(f'files[{i}][file]')
                name = data.get(f'files[{i}][name]', '')
                if file_obj:
                    files_data.append({
                        'name': name,
                        'file': file_obj
                    })
                i += 1
            data['files'] = files_data

            context['request_data'] = data

        return context
