from django.db import models
import uuid
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

def generate_unique_id():
    while True:
        u_id = uuid.uuid4().hex[:4].upper()
        if not Story.objects.filter(story_id=u_id).exists():
            break
    return u_id

class ReadingList(models.Model):
    assigned_user = models.ForeignKey(User, unique=False, default=1, on_delete=models.SET_DEFAULT) # author user model
    reading_list = models.CharField(max_length=1000, blank=True, default='{"reading_list":[]}')

    def __str__(self):
        return f"{self.assigned_user}'s Reading List"

# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=200, default="New Story") # Headline
    author = models.ForeignKey(User, on_delete=models.CASCADE) # author user model

    date = models.DateField(timezone.now, null=True) # Current date
    content = RichTextField(blank=True, null=True)
    story_id = models.CharField(editable=False, max_length=4, default=generate_unique_id, unique=True)

    OPINION = "Opinion"
    SPORTS = "Sports"
    SCHOOL = "School"
    CURRENTEVENTS = "Current Events"

    DELETED = "Deleted"
    DRAFT = "Draft"
    AWAITING_EDITOR_APPROVAL = "Awaiting Editor Approval"
    AWAITING_EDITOR_IN_CHIEF_APPROVAL = "Awaiting Editor In Chief Approval"
    PUBLISHED = "Published"

    category_choices = [(OPINION, "Opinion"),   
                (SPORTS, "Sports"), 
                (SCHOOL, "School"), 
                (CURRENTEVENTS, "Current Events")]

    state_choices = [(DRAFT, "Draft"),   
                (AWAITING_EDITOR_APPROVAL, "Awaiting Editor Approval"), 
                (AWAITING_EDITOR_IN_CHIEF_APPROVAL, "Awaiting Editor In Chief Approval"), 
                (PUBLISHED, "Published"),
                (DELETED, "Deleted")]

    category = models.CharField(max_length=20, choices=category_choices, default=SCHOOL) # Catergory of Article
    state = models.CharField(max_length=50, null=True, blank=True, choices=state_choices, default=DRAFT)
    story_image = models.ImageField(verbose_name='Headline Image', null=True, blank=True, upload_to="images/")

    def __str__(self):
        return f"{self.title} by {self.author} (id:{self.story_id})"

class ClickCounter(models.Model):
    link_name = models.CharField(max_length=20)
    count = models.IntegerField()

    def __str__(self):
        return self.link_name
