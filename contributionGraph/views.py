from django.shortcuts import render
import requests
from django.http import JsonResponse

def home(request):
    # Retrieve the current working URL
    current_url = request.build_absolute_uri()
    return render(request, 'pages/home.html', {'current_url': current_url})

def github_contributions(request):
    try:
        github_token = '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'
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
            'Authorization': f'Bearer {github_token}'
        }

        # Send POST request to GitHub GraphQL API
        response = requests.post(api_url, headers=headers, json={'query': query})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        contribution_data = data.get('data', {}).get('user', {}).get('contributionsCollection', {}).get('contributionCalendar', {})

        return render(request, 'pages/graph.html', {'contribution_data': contribution_data, 'username': username})

    except requests.RequestException as req_error:
        return JsonResponse({'error': f'Request error: {str(req_error)}'}, status=500)

    except Exception as e:
        # Handle any unexpected exception
        error_message = str(e)
        return JsonResponse({'error': error_message}, status=500)
