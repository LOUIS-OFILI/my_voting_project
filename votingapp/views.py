from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from .models import Election, Candidate, Vote, Voter
from django.contrib import messages

from django.db.models import Count


#render homepage
class HomePage(TemplateView):
    template_name = "votingapp/home.html"

    #render user dashboard

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "votingapp/user.html"
    

class Displayballot(LoginRequiredMixin, TemplateView):

    template_name = "votingapp/election_ballot.html"

    def get(self, request):
        elections = Election.objects.all()

        for election in elections:
            election_id = election.id
            election_name = election.election_type
            candidates = Candidate.objects.filter(election=election)

        context = {'election_id': election_id, 'election_name': election_name,
                    'candidates': candidates}
        
        return render(request, self.template_name, context)

class SubmitBallotView(LoginRequiredMixin, View):
    def post(self, request):

        #get the posted candidate Id
        candidate_id = request.POST.get('candidate_id')

        if not candidate_id:
            messages.error(self.request, 'You must choose a candidate to vote for')
            return redirect('voter_ballot')
        
        # grab the Voter's data for checking
        voter =Voter.objects.get(user=request.user)
        if voter.voted:
            messages.error(self.request, 'You have Already Voted!')
            return redirect('voter_ballot')
        else:
            candidate = Candidate.objects.get(id=candidate_id)

            #get the election instance
            election = voter.election

            vote = Vote.objects.create(voter=voter, candidate=candidate, election=election)

            if vote:
                voter.voted = True
                voter.save()
                messages.success(self.request, 'You have Successfully Voted! Thanks')
                return redirect('election_result')
            


# User Ballot List View based on this tutorial 
        # https://www.geeksforgeeks.org/listview-class-based-views-django/    
class UserBallotListView(LoginRequiredMixin, ListView):
   model = Vote
   template_name = "votingapp/ballot_list_view.html"

   def get_queryset(self, *args, **kwargs): 
        
        #get the Voter instance for filtering

        try:
            voter = Voter.objects.get(user=self.request.user)
        except Voter.DoesNotExist:
            voter = None

        if voter:
            return Vote.objects.filter(voter=voter)
        else:
            return Vote.objects.none()
        
        #this view(logic) is for fetching and counting each candidates votes

class ElectionResultsView(LoginRequiredMixin, View):

    template_name = "votingapp/election_results.html"
    def get(self, request):
    #fetch each candidates for an election and count their votes
    #and ensure the candidate with higher vote count comes first
        candidates_vote_count = Candidate.objects.annotate(count_vote=Count('vote')).order_by('-count_vote')

        context = {'candidates_vote_count': candidates_vote_count}
        
        return render(request, self.template_name, context)

    