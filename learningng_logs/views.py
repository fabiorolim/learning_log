from django.shortcuts import render
from .models import Topic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    topics = Topic.objects.order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Adciona um novo assunto"""
    if request.method != 'POST':
        #Nenhum dado submetido, criar formlário em branco
        form = TopicForm()
    else:
        #Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Adciona uma nova entrada sobre assunto"""
    topic = Topic.objects.get(id=topic_id)


    if request.method != 'POST':
        #Formulário vázio
        form = EntryForm()
    else:
        #Processa os dados recebidos via POST
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))


    context = {'topic': topic, 'form': form }
    return render(request, 'learning_logs/new_entry.html', context)