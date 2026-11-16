from django.contrib import admin
from .models import (
    Course, Skill, UserSkill, Question,
    MultipleChoiceQuestion, FillQuestion, CodeQuestion, CodeTestCase,
)

# Register your models here.

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(FillQuestion)
admin.site.register(CodeQuestion)
admin.site.register(CodeTestCase)