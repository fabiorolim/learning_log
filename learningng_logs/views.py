from django.shortcuts import render
from django.utils import log
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    return render(request, 'learning_logs/index.html')



@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user).order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)



@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)



@login_required
def new_topic(request):
    """Adciona um novo assunto"""
    if request.method != 'POST':
        #Nenhum dado submetido, criar formlário em branco
        form = TopicForm()
        context = {'form': form}
        return render(request, 'learning_logs/new_topic.html', context)
    else:
        #Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    """
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
    """



@login_required
def new_entry(request, topic_id):
    """Adciona uma nova entrada sobre assunto"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #Formulário vázio
        form = EntryForm()
    else:
        #Processa os dados recebidos via POST
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form }
    return render(request, 'learning_logs/new_entry.html', context)



@login_required
def edit_entry(request, entry_id):
    """Editada uma entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'form': form, 'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/edit_entry.html', context)
