# play crucial role in handling https requests and definning logic for rendering responses, serves as the controller in the MVC

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from .models import Election, Candidate, Vote, Voter
from django.contrib import messages

from django.db.models import Count
# importations for token based authentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken

#render homepage
class HomePage(TemplateView):
    template_name = "votingapp/home.html"

    #render user dashboard

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "votingapp/user.html"
    

class Displayballot(LoginRequiredMixin, TemplateView):

    template_name = "votingapp/election_ballot.html"

    def get(self, request):
         #fetch the User Token form the AuthToken
        token= AuthToken.objects.create(request.user)[1]
        elections = Election.objects.all()

        for election in elections:
            election_id = election.id
            election_name = election.election_type
            candidates = Candidate.objects.filter(election=election)

        context = {'election_id': election_id, 'election_name': election_name,
                    'candidates': candidates, 'auth_token': token} 
        
        return render(request, self.template_name, context)



#this is for processing the submitted ballot
@method_decorator(csrf_exempt, name='dispatch')
class SubmitBallotView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        #get the posted candidate Id
        candidate_id = request.POST.get('candidate_id')

        if not candidate_id:   
        # when user didnt choose a candidate to vote for
             return Response({'error': 'You must choose a candidate to vote for'}, status=400)
        
        # grab the Voter's data for checking
        try:
         
         voter = Voter.objects.get(user=request.user)

        except Voter.DoesNotExist:
            
            voter = None 

        if voter is None:
             return Response({'error': 'You are not registered for this Election!'}, status=400)

        elif voter is not None and voter.voted:
            return Response({'error': 'You have Already Voted!'}, status=400)
        else:
            candidate = Candidate.objects.get(id=candidate_id)

            #get the election instance
            election = voter.election

            vote = Vote.objects.create(voter=voter, candidate=candidate, election=election)

            if vote:
                voter.voted = True
                voter.save()
                return Response({'success': 'Failed to create vote'}, status=200)
            else:
                 return Response({'error': 'Failed to create vote'}, status=500)
            


# User Ballot List View based on this tutorial 
# https://www.geeksforgeeks.org/listview-class-based-views-django/    
class UserBallotListView(LoginRequiredMixin, ListView):
   model = Vote
   template_name = "votingapp/ballot_list_view.html"

   def get_queryset(self, *args, **kwargs): 
        
        #get the Voter instance for filtering
        # get the logged in user's Voter Info 
        #if the user  is  a registered voter
        # else return none 
        try:
            voter = Voter.objects.get(user=self.request.user)
        except Voter.DoesNotExist:
            voter = None
        #confirm that the logged in user is 
        #a registered voter before filtering his vote data
        if voter:
            return Vote.objects.filter(voter=voter)
        else:
            return Vote.objects.none()
        
        # this view(logic) is for fetching and counting each candidates votes

class ElectionResultsView(LoginRequiredMixin, View):

    template_name = "votingapp/election_results.html"
    def get(self, request):
    #fetch each candidates for an election and count their votes
    #and ensure the candidate with higher vote count comes first
        candidates_vote_count = Candidate.objects.annotate(count_vote=Count('vote')).order_by('-count_vote')
          
          #pass result data to context for use at the template
        context = {'candidates_vote_count': candidates_vote_count}
        
        # render the template and passalong the context data
        return render(request, self.template_name, context)

    