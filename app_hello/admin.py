from django.contrib import admin
from app_hello.models import Profile, Experience, Education, Project, Skill


class SkillsInline(admin.TabularInline):
    model = Skill
    extra = 1


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


# @admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'job_title', 'location')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'job_title')
    list_filter = ('location',)
    inlines = (ProjectInline, EducationInline, ExperienceInline, SkillsInline)

    @admin.display(description='Username', ordering='user__username')
    def username(self, obj):
        return obj.user.username

    admin.site.register(Profile)
    admin.site.register(Experience)
    admin.site.register(Education)
    admin.site.register(Project)
    admin.site.register(Skill)
