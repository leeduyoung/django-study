from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from .models import Candidate, Poll, Choice

import datetime
import logging
from django.db.models import Sum

# Create your views here.
def index(request):
    logging.error('error log test');
    logging.warning('warning log test');

    candidates = Candidate.objects.all()
    context = {'candidates': candidates}
    return render (request, 'elections/index.html', context)

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name=  name)
    # try:
    #     candidate = Candidate.objects.get(name = name)
    # except:
    #     raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    today = datetime.datetime.now()
    
    try:
        poll = Poll.objects.get(area = area, start_date__lte=today, end_date__gte=today)
        candidates = Candidate.objects.filter(area = area)
    except:
        poll = None
        candidates = None

    context = {
        'candidates': candidates,
        'area': area,
        'poll': poll
    }
    return render (request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        print('######',total_votes)
        result['total_votes'] = total_votes['votes__sum']
        rates = []
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id = poll.id, candidate_id = candidate.id)
                rates.append(
                    round(choice.votes / result['total_votes'] * 100,1)
                )
            except:
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = { 'candidates': candidates, 'area': area, 'poll_results': poll_results  }

    return render(request, 'elections/result.html', context)