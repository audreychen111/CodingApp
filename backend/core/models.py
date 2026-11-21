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
  class Meta: #goes inside the model class
    constraints = [
      m.UniqueConstraint(fields=["user", "skill"], name="unique_user_skill"),
    ]
  user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete= m.CASCADE)
  skill= m.ForeignKey(Skill, on_delete= m.CASCADE)
  # belief over skill levels 1-5, e.g. [0.05, 0.15, 0.5, 0.25, 0.05]; empty until first practice
  belief = m.JSONField(default=list)
  level = m.FloatField(default=0.0)
  answer_counts = m.PositiveIntegerField(default=0)
  update_at = m.DateTimeField(auto_now=True)


class Question(m.Model):
  class QuestionType(m.TextChoices):
    MCQ = 'mcq', 'Multiple Choice'
    FILL = 'fill', 'Fill in the Blank'
    CODE = 'code', 'Coding'
  prompt = m.TextField()
  type = m.CharField(max_length=255, choices=QuestionType)
  skill = m.ForeignKey(Skill, on_delete=m.CASCADE)
   # Elo rating: starts from difficulty set by the import, then updated after each answer
  difficulty = m.FloatField(null=True, blank=True)
  n_attempts = m.PositiveIntegerField(default=0)

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

class Attempt(m.Model):
  user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
  question = m.ForeignKey(Question, on_delete=m.CASCADE)
  answer = m.TextField(blank=True)
  correct = m.BooleanField()
  expected = m.FloatField(null=True, blank=True)  # predicted P(correct) before answering
  seconds_taken = m.PositiveIntegerField(null=True, blank=True)
  created_at = m.DateTimeField(auto_now_add=True)