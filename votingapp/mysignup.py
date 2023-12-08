from django import forms
from allauth.account.forms import SignupForm
from .models import UserProfile
import requests

# extend the allauth signup form
# to add other fields
class CustomRegistrationForm(SignupForm):
    #add a full name field to the registration form
    full_name = forms.CharField(
        max_length=35,
        label='Full Name'
       
    )
    
    #add a BVN field to the registration form
    bvn = forms.CharField(max_length=11)


    # Make API Call to verify supplied BVN
    def clean_bvn(self):

        #grab the bvn
        bvn = self.cleaned_data['bvn']


        # BVN verification endpoint from youverify.co
        url = "https://api.sandbox.youverify.co/v2/api/identity/ng/bvn"

        # API Token set as in the request header
        headers = {
            "Token": "NyDLCnCB.zS59PFMfqSFNz6tn6jaiDNqkBJ6rfkqCLLmi",
        }


         # Required Body Parameters: Valid BVN 
         # and isSubjectConsent passed to the data 
         #parameter
        data = {
            "id": bvn,
            "isSubjectConsent": True,
        }

        
        #make API call with Python requests module
        response = requests.post(url, headers=headers, data=data)
        
        #check if the BVN verification was not successful
        # and if not successful, raise form validation exception
        # with message
        if response.status_code != 200:
            raise forms.ValidationError('BVN validation failed. Please provide a valid BVN.')

        return bvn




    def save(self, request):

        user = super(CustomRegistrationForm, self).save(request)

        user_profile = UserProfile.objects.create(
        user=user,
        full_name=self.cleaned_data['full_name'],
        bvn=self.cleaned_data['bvn']
        )
        
        return user