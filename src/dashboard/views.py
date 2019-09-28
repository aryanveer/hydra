from django.views import View
from django.contrib.auth.decorators import login_required
from users.models import Keywords
import json
from django.shortcuts import render, redirect


# class Home(View):
#
# 	def get(self, request):
# 		return render(request, 'dashboard/base.html')

@login_required(login_url='/login/')
def dashboard(request):
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
		print(similar_words, new_keyword, source, priority)
		return redirect('/dashboard/channel-monitoring')


@login_required(login_url='/login/')
def delete_keyword(request, keyword):
	return render(request, 'dashboard/base.html')