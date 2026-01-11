"""
US State Population Data (2024 Census Bureau Estimates)
Source: US Census Bureau Population Estimates Program
Used for per capita rate calculations
"""

# 2024 Census Bureau estimates (most recent available)
# Source: https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html
US_STATE_POPULATIONS = {
    'Alabama': 5108468,
    'Alaska': 733406,
    'Arizona': 7431344,
    'Arkansas': 3067732,
    'California': 38965193,
    'Colorado': 5877610,
    'Connecticut': 3617176,
    'Delaware': 1031890,
    'District of Columbia': 678972,
    'Florida': 23372215,
    'Georgia': 11029227,
    'Hawaii': 1435138,
    'Idaho': 1964726,
    'Illinois': 12516863,
    'Indiana': 6862199,
    'Iowa': 3207004,
    'Kansas': 2940546,
    'Kentucky': 4526154,
    'Louisiana': 4573749,
    'Maine': 1395722,
    'Maryland': 6180253,
    'Massachusetts': 7001399,
    'Michigan': 10037261,
    'Minnesota': 5737915,
    'Mississippi': 2939690,
    'Missouri': 6196156,
    'Montana': 1132812,
    'Nebraska': 1978379,
    'Nevada': 3194176,
    'New Hampshire': 1402054,
    'New Jersey': 9290841,
    'New Mexico': 2114371,
    'New York': 19571216,
    'North Carolina': 10835491,
    'North Dakota': 783926,
    'Ohio': 11785935,
    'Oklahoma': 4053824,
    'Oregon': 4233358,
    'Pennsylvania': 12961683,
    'Rhode Island': 1095962,
    'South Carolina': 5373555,
    'South Dakota': 919318,
    'Tennessee': 7126489,
    'Texas': 30503301,
    'Utah': 3417734,
    'Vermont': 647464,
    'Virginia': 8683619,
    'Washington': 7812880,
    'West Virginia': 1770071,
    'Wisconsin': 5910955,
    'Wyoming': 584057,
}

# State abbreviations for mapping
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def get_population(state_name):
    """Get population for a state."""
    return US_STATE_POPULATIONS.get(state_name, None)

def get_abbrev(state_name):
    """Get state abbreviation."""
    return STATE_ABBREV.get(state_name, None)

