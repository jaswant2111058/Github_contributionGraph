from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from django.conf import settings



def home(request):
    # Retrieve the current working URL
    current_url = request.build_absolute_uri()
    return render(request, 'pages/home.html', {'current_url': current_url})
def github_contributions(request):
    try:
        
        github_token = "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"
        username = request.GET.get('username')

        if not username:
            raise ValueError("Username parameter is missing.")

        # GraphQL query to get the user's contribution data
        query = """
            query {
                user(login: "%s") {
                    contributionsCollection {
                        contributionCalendar {
                            totalContributions
                            weeks {
                                contributionDays {
                                    contributionCount
                                }
                            }
                        }
                    }
                }
            }
        """ % username

        api_url = 'https://api.github.com/graphql'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % github_token
        }

        # Send POST request to GitHub GraphQL API
        response = requests.post(api_url, headers=headers, json={'query': query})

        if response.status_code == 200:
            data = response.json()
            contribution_data = data.get('data', {}).get('user', {}).get('contributionsCollection', {}).get('contributionCalendar', {})
            return render(request, 'pages/graph.html', {'contribution_data': contribution_data,'username':username})
        else:
            error_message = data.get('message', 'Failed to fetch GitHub data')
            raise ValueError(f"GitHub API error: {error_message}")

    except Exception as e:
        # Handle any unexpected exception
        error_message = str(e)
        return JsonResponse({'error': "No username Exist"}, status=500)
