from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from .models import Election, Candidate, Vote, Voter
from django.contrib import messages

# Create your views here.

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
                return redirect('voter_ballot')
    