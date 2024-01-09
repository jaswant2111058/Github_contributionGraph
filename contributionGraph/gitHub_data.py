import requests
from django.http import JsonResponse
from datetime import datetime
import re


 
def calculate_time_taken(open_date, close_date):
    try:
        if open_date and close_date:
            open_time = datetime.strptime(open_date, "%Y-%m-%dT%H:%M:%SZ")
            close_time = datetime.strptime(close_date, "%Y-%m-%dT%H:%M:%SZ")
            time_taken = str(close_time - open_time)
            return time_taken
        else:
            return None
    except Exception as e:
        print(f"Error in calculate_time_taken: {e}")
        return None





def get_previous_and_next_comments(comments, comment_id):
    try:
        previous_comment = None
        next_comment = None

        for i, comment in enumerate(comments):
            if comment['id'] == comment_id:
                if i > 0:
                    previous_comment = comments[i - 1]
                if i < len(comments) - 1:
                    next_comment = comments[i + 1]
                break

        return previous_comment, next_comment
    except Exception as e:
        print(f"Error in get_previous_and_next_comments: {e}")
        return None, None









def get_modified_files_functions_classes(owner, repo, issue_number, token):
    try:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        modified_details = []

        
        files_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{issue_number}/files'
        files_response = requests.get(files_url, headers=headers)
        pr_files_data = files_response.json()
    

        for pr_file_data in pr_files_data:
                try:
                    if 'filename' in pr_file_data and 'additions' in pr_file_data and 'deletions' in pr_file_data:
                        file_path = pr_file_data['filename']
                        additions = pr_file_data['additions']
                        deletions = pr_file_data['deletions']
                        changes = additions + deletions
                        file_data = {
                                'file_path':file_path,
                                'issue_id':issue_number,
                                'changes': changes,
                                'deletions': deletions,
                                'additions':additions, 
                            }
                        modified_details.append(file_data)
                except Exception as inner_e:
                    print(f"Error processing file data: {inner_e}\nFile data: {pr_file_data}")
        return modified_details
    except Exception as e:
        print(f"Error in get_modified_files_functions_classes: {e}")
        return {}



def get_issue_comments(owner, repo, issue_number, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        comments = response.json()
        filtered_comments = []

        for comment in comments:
            filtered_comment = {
                'issue_id':issue_number,
                'id': comment['id'],
                'user':  comment['user']['login'],
                'created_at': comment['created_at'],
                'updated_at': comment['updated_at'],
                'author_association': comment['author_association'],
                'body': comment['body']
            }
            filtered_comments.append(filtered_comment)

        return filtered_comments
    else:
        print(f"Error retrieving comments. Status code: {response.status_code}")
        return []


def get_issue_labels(owner, repo, issue_number, token):
    labels_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    labels_response = requests.get(labels_url, headers=headers)

    if labels_response.status_code == 200:
        labels_details = labels_response.json()
        labels = []

        for label in labels_details:
            label['issue_id'] = issue_number
            labels.append(label)

        return labels
    else:
        print(f"Error retrieving labels. Status code: {labels_response.status_code}")
        return []









def replace_none_with_null(value):
    return "null" if value is None else value

def get_all_issues_details(owner, repo, token, perpage, pageno):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/issues'
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        params = {
            'per_page': perpage,
            'page': pageno  # Add this parameter to specify the page number
        }
        response = requests.get(url, headers=headers, params=params)
        issues = response.json()
        all_issues_details = []

        for issue in issues:
            issue_number = issue['number']

            # Get issue comments
            comments = replace_none_with_null(get_issue_comments(owner, repo, issue_number, token))

            # Get modified files, functions, and classes
            modified_details = replace_none_with_null(get_modified_files_functions_classes(owner, repo, issue_number, token))

            # Get issue labels
            labels = replace_none_with_null(get_issue_labels(owner, repo, issue_number, token))

            # Calculate time taken for the issue to be closed
            time_taken = replace_none_with_null(calculate_time_taken(issue['created_at'], issue['closed_at']))

            # Processed title and body
            processed_title = replace_none_with_null(issue['title'].lower().replace(' ', '_')) if issue['title'] else None
            processed_body = replace_none_with_null(issue['body'].lower()) if issue['body'] else None

            all_issues_details.append({
                'issue_id': issue_number,
                'title': replace_none_with_null(issue['title']),
                'author': replace_none_with_null(issue['user']['login']),
                'open_date': replace_none_with_null(issue['created_at']),
                'close_date': replace_none_with_null(issue['closed_at']),
                'body': replace_none_with_null(issue['body']),
                'time_taken': time_taken,
                'closed_by': replace_none_with_null(issue['closed_by']['login']) if 'closed_by' in issue and issue['closed_by'] else None,
                'processed_title': processed_title,
                'processed_body': processed_body,
                'comments': comments,
                'modified_details': modified_details,
                'labels': labels
            })

        return all_issues_details

    except Exception as e:
        print(f"Error in get_all_issues_details: {e}")
        return []




