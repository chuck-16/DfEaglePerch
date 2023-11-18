from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from .models import Story, ReadingList, ClickCounter
from django.contrib.auth.models import User, Group
from django.contrib import messages
from datetime import date
from .forms import NewUserForm
import json
from .forms import StoryForm


# Create your views here.
def homepage(request):
    stories = Story.objects.all().filter(state="Published").order_by('date').reverse()
    image_stories = Story.objects.all().filter(state="Published").order_by('date').reverse()
    for story in stories:
        if not story.story_image:
            image_stories = image_stories.exclude(story_id=story.story_id)
        else:
            stories = stories.exclude(story_id=story.story_id)
    featured_story = image_stories[0]
    image_stories = image_stories.exclude(story_id=featured_story.story_id)

    return render(request = request,
                  template_name='main/homepage.html',
                  context={'feature_stories':stories[0:5],
                            'image_feature_stories':image_stories[0:3],
                            'date':date.today(),
                            'featured_story':featured_story})

def category_view(request, category):
    return render(request = request,
                  template_name='main/category.html',
                  context={'stories':Story.objects.all().filter(category=category, state="Published").order_by('date').reverse(),
                            'date':date.today(),
                            'category':category})

def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        return render(request = request,
                  template_name='main/search.html',
                  context={'stories':Story.objects.filter(title__icontains=query, state="Published").order_by('date').reverse(),
                            'date':date.today(),
                            'query':query})
    

def logout_request(request):
    messages.success(request, f'Logged out of "{request.user}"')
    logout(request)
    return redirect("homepage")

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            user_reading_list = ReadingList(assigned_user=user)
            user_reading_list.save()

            login(request, user)
            messages.success(request, f'Registered "{request.user}"')
            return redirect("homepage")

        else:
            messages.error(request, f'Registration information incorrect')
            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form,
                                    "request":request,
                                    'date':date.today()})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form,
                            "request":request,
                            'date':date.today()})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged into "{request.user}"')
                return redirect('/')
        else:
            messages.error(request, f'Login information incorrect')
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form,
                            "request":request,
                            'date':date.today()})

def story_view(request, id):
    user = request.user
    user_reading_list = []
    in_reading_list = False

    if user.is_authenticated:
        user_reading_list = ReadingList.objects.all().get(assigned_user=user)
        reading_list = json.loads(user_reading_list.reading_list)["reading_list"]
        in_reading_list = id in reading_list

    if request.method == 'POST':
        if in_reading_list:
            reading_list.remove(id)
        else:
            reading_list.append(id)
        user_reading_list.reading_list = json.dumps({"reading_list":reading_list})
        user_reading_list.save() 
        return redirect(f'/story/{id}')
    story = Story.objects.all().get(story_id=id)
    more_from_author = []
    more_from_category = []

    if len(Story.objects.all().filter(author=story.author)) > 1:
        more_from_author.extend(Story.objects.all().filter(author=story.author, state="Published").exclude(story_id=story.story_id).order_by('date').reverse())
    if len(Story.objects.all().filter(category=story.category).exclude(story_id=story.story_id)) > 1:
        more_from_category.extend(Story.objects.all().filter(category=story.category, state="Published").exclude(author=story.author).order_by('date').reverse())
    
    return render(request = request,
                  template_name='main/story.html',
                  context={'story':story,
                            'date':date.today(),
                            'in_reading_list':in_reading_list,
                            'more_from_author':more_from_author,
                            'more_from_category':more_from_category})

def phone_story(request, id):
    user = request.user

    return render(request = request,
                  template_name='main/phone_story.html',
                  context={'story':Story.objects.all().get(story_id=id),
                            'date':date.today()})

@login_required
def profile_view(request, id):
    user = User.objects.get(username=id)
    reading_list = []
    for story_id in json.loads(ReadingList.objects.all().get(assigned_user=user).reading_list)['reading_list']:
        try:
            reading_list.append(Story.objects.all().filter(state="Published").get(story_id=story_id))
        except:
            continue
    
    return render(request = request,
                  template_name='main/profile.html',
                  context={'user':user,
                        'date':date.today(),
                        'reading_list':reading_list,
                        'writing_list':Story.objects.all().filter(author=user, state="Published").order_by('date').reverse()})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists() or u.groups.filter(name='Editor').exists() or u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def writer_view(request):
    user = request.user

    return render(request = request,
                  template_name='main/writer.html',
                  context={'user':user,
                        'date':date.today(),
                        'drafts':Story.objects.all().filter(author=user, state="Draft"),
                        'awaiting_supervisor_approval':Story.objects.all().filter(author=user, state="Awaiting Editor In Chief Approval").order_by('date'),
                        'awaiting_editor_approval':Story.objects.all().filter(author=user, state="Awaiting Editor Approval").order_by('date'),
                        'published':Story.objects.all().filter(author=user, state="Published").order_by('date').reverse()})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists() or u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def editor_view(request):
    user = request.user

    return render(request = request,
                  template_name='main/editor.html',
                  context={'user':user,
                        'date':date.today(),
                        'awaiting_approval':Story.objects.all().filter(state="Awaiting Editor Approval").order_by('date'),
                        'awaiting_supervisor_approval': Story.objects.all().filter(state="Awaiting Editor In Chief Approval").order_by('date'),
                        'published':Story.objects.all().filter(state="Published").order_by('date').reverse(),
                        'users':User.objects.filter(groups__isnull=True).exclude(username=user),
                        'writers':User.objects.filter(groups__name="Writer").exclude(username=user),
                        'editors':User.objects.filter(groups__name="Editor").exclude(username=user)})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def supervisor_view(request):
    user = request.user

    return render(request = request,
                  template_name='main/supervisor.html',
                  context={'user':user,
                        'date':date.today(),
                        'awaiting_approval':Story.objects.all().filter(state="Awaiting Editor In Chief Approval").order_by('date'),
                        'published':Story.objects.all().filter(state="Published").order_by('date').reverse(),
                        'users':User.objects.filter(groups__isnull=True).exclude(username=user),
                        'writers':User.objects.filter(groups__name="Writer").exclude(username=user),
                        'editors':User.objects.filter(groups__name="Editor").exclude(username=user),
                        'supervisors':User.objects.filter(groups__name="Editor In Chief").exclude(username=user)})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists() or u.groups.filter(name='Editor').exists() or u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def edit_story(request, id):
    editing_story = Story.objects.all().get(story_id=id)
    form = StoryForm(request.POST or None, request.FILES or None,instance=editing_story)
    if form.is_valid():
        form.save()
    return render(request = request,
                  template_name='main/edit_story.html',
                  context={'story':editing_story,
                            'date':date.today(),
                            "form":form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists() or u.groups.filter(name='Editor').exists() or u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def new_draft(request):
    draft = Story(author=request.user, date=date.today())
    draft.save()
    messages.success(request, f'Made draft "{draft.title}"')
    return redirect('writer_view')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor').exists() or u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def change_state(request, id, new_state, redirect_page):
    change_story = Story.objects.all().get(story_id=id)
    change_story.state = new_state
    change_story.save()
    messages.success(request, f'Made "{change_story.title}" into a "{new_state}" story')
    return redirect(redirect_page)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def change_group(request, id, new_group, redirect_page):
    change_user = User.objects.all().get(id=id)

    new_user_group = Group.objects.get_or_create(name=new_group)[0].id

    if change_user.groups.all().exists():
        old_user_group = change_user.groups.all()[0].id

        change_user.groups.add(new_user_group)
        change_user.groups.remove(old_user_group)
        change_user.save()
        messages.success(request, f'Made user "{change_user}" into a "{new_group}"')
    else:
        change_user.groups.add(new_user_group)
        change_user.save()
        messages.success(request, f'Made user "{change_user}" into a "{new_group}"')
    
    return redirect(redirect_page)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Editor In Chief').exists() or u.groups.filter(name='Developer').exists())
def remove_group(request, id, redirect_page):
    change_user = User.objects.all().get(id=id)

    old_user_group = change_user.groups.all()[0].id
    
    change_user.groups.remove(old_user_group)
    change_user.save()
    return redirect(redirect_page)

def pass_on(request, href):
    if href == "Piccola":
        new_click = ClickCounter.objects.all().get(link_name=href)
        new_click.count += 1
        new_click.save()
        return redirect("https://piccolany.com/")
    if href == "Cocoa Tree":
        new_click = ClickCounter.objects.all().get(link_name=href)
        new_click.count += 1
        new_click.save()
        return redirect("https://www.cocoatreechocolates.com/")

