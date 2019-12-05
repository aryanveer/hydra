from django.views import View
from django.contrib.auth.decorators import login_required
from users.models import Keywords
import json
from django.shortcuts import render, redirect
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class Home(View):

	def get(self, request):
		graph_data = "10,10,10,10,10,10,10,20,30,10,12,50,10"
		return render(request, 'dashboard/home.html', {"data": graph_data})


@login_required(login_url='/login/')
def dashboard(request):
	print("hello")
	return render(request, 'dashboard/base.html')


@login_required(login_url='/login/')
def channel_monitoring(request):

	group = request.user.groups.values_list('id', flat=True).first()

	if request.method == 'GET':
		keywords = Keywords.objects.filter(group_id=group).values('keyword', 'source', 'priority', 'similar_keywords')
		test_all = json.dumps({"data": list(keywords)})
		data = {'test_data': test_all, }
		return render(request, 'dashboard/keywords.html', data)

	if request.method == 'POST':
		new_keyword = request.POST.get('new_keyword')
		source = request.POST.get('source')
		priority = request.POST.get('priority')
		similar_words = request.POST.get('similar_words')
		Keywords(keyword=new_keyword, source=source, priority=priority, similar_keywords=similar_words, group_id=group).save()
		return redirect('/dashboard/channel-monitoring')


@login_required(login_url='/login/')
def delete_keyword(request):
	keyword = request.GET['key']
	group = request.user.groups.values_list('id', flat=True).first()

	instance = Keywords.objects.get(keyword=keyword, group_id=group)
	instance.delete()
	return redirect('/dashboard/channel-monitoring')


@login_required(login_url='/login/')
def update_keyword(request):
	new_keyword = request.POST.get('new_keyword')
	source = request.POST.get('source')
	priority = request.POST.get('priority')
	similar_words = request.POST.get('similar_words')

	keyword = request.GET['key']
	group = request.user.groups.values_list('id', flat=True).first()
	instance = Keywords.objects.get(keyword=keyword, group_id=group)
	instance.keyword = new_keyword
	instance.source = source
	instance.priority = priority
	instance.similar_keywords = similar_words
	instance.save()
	return redirect('/dashboard/channel-monitoring')


def blah(request):
	_es = None
	_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	data = {"name": "Aryan", "age": 22, "experienceInYears": 1}
	data = json.dumps(data)
	_es.index(index='hydra', doc_type='keywords', body=data)
	# if _es.ping():
	# 	print('Yay Connect')
	# else:
	# 	print('Awww it could not connect!')
	# print(_es)
	s = Search(using=_es, index='hydra', doc_type='keywords').query("match", age="22")
	response = s.execute()
	# response = s.scan()
	# for commit in response:
	# 	print(commit.name, commit.age, commit.experienceInYears)
	#a = s.source(['name', 'age']).scan()
	for commit in response:
		print(commit.name, commit.age, commit.experienceInYears)