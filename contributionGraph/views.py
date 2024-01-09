from django.shortcuts import render
import requests
from django.http import JsonResponse
import re

from .gitHub_data import get_all_issues_details
from .csvConverter import write_issues_to_csv, write_comment_to_csv, write_modified_file_to_csv, write_label_to_csv


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


def github_data(request):
    try:
        repo_url = request.GET.get('repo_url')
        perpage = request.GET.get('perpage')
        pageno = request.GET.get('pageno')
        token = request.GET.get('token')
        
        print(repo_url,perpage,pageno,token)

        if not repo_url:
            raise ValueError("repo_url parameter is missing.")
        match = re.search(r'https://github.com/([^/]+)/([^/]+)(/)?$', repo_url)
        if not match:
            raise ValueError('Invalid GitHub repository link')

        owner = match.group(1)
        repo = match.group(2)

        all_issues_details = get_all_issues_details(owner, repo, token, perpage, pageno)

        issues_details = []

        for issue in all_issues_details:
            issue_detail = {
                'issue_id': issue['issue_id'],
                'title': issue['title'],
                'author': issue['author'],
                'open_date': issue['open_date'],
                'close_date': issue['close_date'],
                'body': issue['body'],
                'time_taken': issue['time_taken'],
                'closed_by': issue['closed_by'],
                'processed_title': issue['processed_title'],
                'processed_body': issue['processed_body'],
            }
            issues_details.append(issue_detail)
        
        
        
        comment_details = []
        for comment in all_issues_details:
            comment_details = comment_details+comment['comments']
            
            
            
             
        modified_file_detail = [] 
        for file_detail in all_issues_details:
            modified_file_detail =modified_file_detail+ (file_detail['modified_details'])
            
        
        
        labels_detail =[]
        for label in all_issues_details:
            labels_detail = labels_detail+(label['labels'])
            
        
        write_issues_to_csv(issues_details,owner, repo, perpage, pageno)
        write_comment_to_csv(comment_details,owner, repo, perpage, pageno)
        write_modified_file_to_csv(modified_file_detail,owner, repo, perpage, pageno)
        write_label_to_csv(labels_detail,owner, repo, perpage, pageno)

        return JsonResponse(all_issues_details, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
