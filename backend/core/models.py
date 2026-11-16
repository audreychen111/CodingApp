from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models as m

# id column is automatically created by django if no pk is specified
# '_id' is added to the column name for foreign keys, don't do it twice

class Course(m.Model):
  name = m.CharField(max_length=255, unique=True)

class Skill(m.Model):
  class Meta:
    constraints = [m.UniqueConstraint(fields=["course", "name"], name="unique_course_skill")]
  name = m.CharField(max_length=255)
  course = m.ForeignKey(Course, on_delete=m.CASCADE)

class UserSkill(m.Model):
  class Meta:
    constraints = [m.UniqueConstraint(fields=["user", "skill"], name="unique_user_skill")]
  user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
  skill = m.ForeignKey(Skill, on_delete=m.CASCADE)
  level = m.FloatField(default=0.0)

class Question(m.Model):
  class QuestionType(m.TextChoices):
    MCQ = 'mcq', 'Multiple Choice'
    FILL = 'fill', 'Fill in the Blank'
    CODE = 'code', 'Coding'
  prompt = m.TextField()
  type = m.CharField(max_length=255, choices=QuestionType)
  skill = m.ForeignKey(Skill, on_delete=m.CASCADE)
  difficulty = m.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

# can let an empty string represent no option (eg if we only want to give 2 options)
class MultipleChoiceQuestion(m.Model):
  question = m.OneToOneField(Question, on_delete=m.CASCADE)
  option_a = m.CharField(max_length=255)
  option_b = m.CharField(max_length=255)
  option_c = m.CharField(max_length=255, blank=True)
  option_d = m.CharField(max_length=255, blank=True)
  answer = m.CharField(max_length=1, choices=[("A", "A"),("B", "B"),("C", "C"),("D", "D")])

class FillQuestion(m.Model):
  question = m.OneToOneField(Question, on_delete=m.CASCADE)
  answer = m.CharField(max_length=255)

class CodeQuestion(m.Model):
  question = m.OneToOneField(Question, on_delete=m.CASCADE)
  starter_code = m.TextField(blank=True)
  reference_solution = m.TextField()

class CodeTestCase(m.Model):
  question = m.ForeignKey(CodeQuestion, on_delete=m.CASCADE, related_name="test_cases")
  input = m.TextField(blank=True)
  expected_output = m.TextField()
  is_hidden = m.BooleanField(default=True)