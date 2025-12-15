from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, ReferenceField, ListField
from mongoengine.fields import UUIDField

# MongoDB Models using mongoengine

class Sondage(Document):
    title = StringField(max_length=200, required=True)
    description = StringField(required=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
    user_id = IntField(required=True)  # Store Django User ID as integer
    primary_color = StringField(max_length=7, default="#4F46E5")
    background_color = StringField(max_length=7, default="#ffffff")
    font_family = StringField(max_length=100, default="Poppins")
    shareable_link = UUIDField(default=uuid.uuid4, unique=True)
    password = StringField(max_length=100, null=True)
    limit_responses = BooleanField(default=False)
    limit_ip = BooleanField(default=True)
    
    meta = {'collection': 'sondages'}

    def __str__(self):
        return self.title
    
    @property
    def user(self):
        from django.contrib.auth.models import User
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    @property
    def questions(self):
        return Question.objects(sondage=self)

class Question(Document):
    QUESTION_TYPES = [
        ('sc', 'Single Choice'),
        ('mc', 'Multiple Choice'),
        ('tx', 'Text'),
        ('scal','echelle (1-5)'),
    ]

    sondage = ReferenceField(Sondage, reverse_delete_rule=2, required=True)  # CASCADE = 2
    text = StringField(max_length=200, required=True)
    question_type = StringField(max_length=4, choices=QUESTION_TYPES, required=True)
    required = BooleanField(default=True)
    min_value = IntField(null=True)
    max_value = IntField(null=True)
    
    meta = {'collection': 'questions'}

    def __str__(self):
        return self.text
    
    @property
    def scale_range(self):
        if self.question_type == 'scal' and self.min_value is not None and self.max_value is not None:
            return range(self.min_value, self.max_value + 1)
        return []
    
    @property
    def choices(self):
        return Choice.objects(question=self)


class Choice(Document):
    question = ReferenceField(Question, reverse_delete_rule=2, required=True)  # CASCADE = 2
    text = StringField(max_length=200, required=True)
    
    meta = {'collection': 'choices'}
    
    def __str__(self):
        return self.text


class Reponse(Document):
    sondage = ReferenceField(Sondage, reverse_delete_rule=2, required=True)  # CASCADE = 2
    date = DateTimeField(default=timezone.now)
    user_id = IntField(null=True)  # Store Django User ID as integer
    ip_address = StringField(null=True)
    answer = StringField(max_length=255, default='')
    created_at = DateTimeField(default=timezone.now)
    
    meta = {'collection': 'reponses'}
    
    @property
    def user(self):
        if self.user_id:
            from django.contrib.auth.models import User
            try:
                return User.objects.get(id=self.user_id)
            except User.DoesNotExist:
                return None
        return None

class Answer(Document):
    reponse = ReferenceField(Reponse, reverse_delete_rule=2, required=True)  # CASCADE = 2
    question = ReferenceField(Question, reverse_delete_rule=2, required=True)  # CASCADE = 2
    choix = ListField(ReferenceField(Choice), default=list)  # For multiple choices
    texte = StringField(null=True)  # For free text answers
    
    meta = {'collection': 'answers'}