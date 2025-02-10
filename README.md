# Plan Eligibility Checker

A simple Python application that checks eligibility criteria for healthcare plans using the CMS Marketplace API.

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add your CMS API key:
```
CMS_API_KEY=your_api_key_here
```

To get an API key, visit: https://developer.cms.gov/marketplace-api/key-request.html

## Usage

Run the application:
```bash
python src/plan_eligibility.py
```

The application will prompt you for:
1. HIOS ID (Plan ID)
2. ZIP Code
3. Plan Year

It will then display the eligibility criteria for the specified plan.

## Output

The application will return the following eligibility criteria:
- Plan name
- Metal level
- Market type
- Maximum age for child dependents
- List of eligible dependent relationships
- Service area ID
- National network availability
- Specialist referral requirements

## Error Handling

The application handles various error cases:
- Invalid API key
- Invalid plan ID
- Invalid ZIP code
- Network errors
- API errors

## API Documentation

This application uses the CMS Marketplace API. For full API documentation, visit:
https://marketplace.api.healthcare.gov/api-docs/ 