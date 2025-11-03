from django.contrib import admin
from .models import (
    Task, TaskAttachment, TaskNote,
    ReelsIdea, ReelsExampleLink,
    MasterClassIdea, MasterClassMaterial, MasterClassExampleLink, MasterClassFile, MasterClassDate
)

class TaskAttachmentInline(admin.TabularInline):
    model = TaskAttachment
    extra = 1


class TaskNoteInline(admin.TabularInline):
    model = TaskNote
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "is_completed", "is_urgent", "is_hidden", "created_at")
    list_filter = ("is_completed", "is_urgent", "is_hidden")
    search_fields = ("title", "description")
    inlines = [TaskAttachmentInline, TaskNoteInline]


class ReelsExampleLinkInline(admin.TabularInline):
    model = ReelsExampleLink
    extra = 1


@admin.register(ReelsIdea)
class ReelsIdeaAdmin(admin.ModelAdmin):
    list_display = ("reels_number", "title", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("reels_number", "title")
    inlines = [ReelsExampleLinkInline]


class MasterClassMaterialInline(admin.TabularInline):
    model = MasterClassMaterial
    extra = 1


class MasterClassExampleLinkInline(admin.TabularInline):
    model = MasterClassExampleLink
    extra = 1


class MasterClassFileInline(admin.TabularInline):
    model = MasterClassFile
    extra = 1


class MasterClassDateInline(admin.TabularInline):
    model = MasterClassDate
    extra = 1


@admin.register(MasterClassIdea)
class MasterClassIdeaAdmin(admin.ModelAdmin):
    list_display = ("mk_number", "title", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("mk_number", "title")
    inlines = [
        MasterClassMaterialInline,
        MasterClassExampleLinkInline,
        MasterClassFileInline,
        MasterClassDateInline,
    ]
