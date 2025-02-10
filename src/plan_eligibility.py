import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PlanEligibilityChecker:
    def __init__(self):
        self.api_key = os.getenv('CMS_API_KEY')
        self.base_url = "https://marketplace.api.healthcare.gov/api/v1"
        
        # Debug print
        print(f"Using API key: {self.api_key}")
        
        if not self.api_key:
            raise ValueError("CMS_API_KEY environment variable is required")
        if self.api_key == "your_api_key_here":
            raise ValueError("Please update the CMS_API_KEY in .env with your actual API key")

    def get_county_fips(self, zipcode, year):
        """Get county FIPS code from zipcode"""
        url = f"{self.base_url}/counties/by/zip/{zipcode}"
        params = {
            'apikey': self.api_key,
            'year': year
        }
        
        # Debug print
        print(f"\nMaking request to: {url}")
        print(f"With parameters: {params}")
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"\nError Response: {response.text}")
        response.raise_for_status()
        
        counties = response.json().get('counties', [])
        if not counties:
            raise ValueError(f"No counties found for zipcode {zipcode}")
            
        return counties[0]['fips']

    def get_plan_details(self, plan_id, year):
        """Get basic plan details including eligibility criteria"""
        url = f"{self.base_url}/plans/{plan_id}"
        params = {
            'apikey': self.api_key,
            'year': year
        }
        
        # Debug print
        print(f"\nMaking request to: {url}")
        print(f"With parameters: {params}")
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"\nError Response: {response.text}")
        response.raise_for_status()
        
        return response.json().get('plan', {})

    def extract_eligibility_criteria(self, plan_details):
        """Extract relevant eligibility criteria from plan details"""
        eligibility = {
            'plan_name': plan_details.get('name'),
            'metal_level': plan_details.get('metal_level'),
            'market_type': plan_details.get('market'),
            'max_age_child': plan_details.get('max_age_child'),
            'eligible_dependents': [],
            'service_area_id': plan_details.get('service_area_id'),
            'has_national_network': plan_details.get('has_national_network', False),
            'specialist_referral_required': plan_details.get('specialist_referral_required', False)
        }
        
        # Extract eligible dependent relationships if available
        issuer = plan_details.get('issuer', {})
        if issuer:
            eligibility['eligible_dependents'] = issuer.get('eligible_dependents', [])
        
        return eligibility

    def check_plan_eligibility(self, plan_id, zipcode, year):
        """Main function to check plan eligibility criteria"""
        try:
            # Get plan details
            plan_details = self.get_plan_details(plan_id, year)
            
            # Extract eligibility criteria
            eligibility_criteria = self.extract_eligibility_criteria(plan_details)
            
            return {
                'success': True,
                'eligibility_criteria': eligibility_criteria,
                'complete_response': plan_details  # Add the complete API response
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    # Example usage
    checker = PlanEligibilityChecker()
    
    # Example inputs
    plan_id = input("Enter HIOS ID (e.g., 11512NC0100031): ")
    zipcode = input("Enter ZIP code: ")
    year = int(input("Enter plan year: "))
    
    result = checker.check_plan_eligibility(plan_id, zipcode, year)
    
    if result['success']:
        print("\nEligibility Criteria:")
        for key, value in result['eligibility_criteria'].items():
            print(f"{key}: {value}")
    else:
        print(f"\nError: {result['error']}")

if __name__ == "__main__":
    main() 