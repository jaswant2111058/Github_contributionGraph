import csv
import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_issues_to_csv(issues_data, owner, repo, perpage, pageno):
    directory = f'{owner}/{repo}'
    ensure_directory_exists(directory)

    with open(f'{directory}/{perpage}_{pageno}_issues_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'issue_id',
            'title',
            'author',
            'open_date',
            'close_date',
            'body',
            'time_taken',
            'closed_by',
            'processed_title',
            'processed_body'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()
        
        for issue_data in issues_data:
            writer.writerow(issue_data)

def write_comment_to_csv(issues_data, owner, repo, perpage, pageno):
    directory = f'{owner}/{repo}'
    ensure_directory_exists(directory)

    with open(f'{directory}/{perpage}_{pageno}_comment_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'issue_id',
            'id',
            'user',
            'created_at',
            'updated_at',
            'author_association',
            'body'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for issue_data in issues_data:
            writer.writerow(issue_data)

def write_modified_file_to_csv(issues_data, owner, repo, perpage, pageno):
    directory = f'{owner}/{repo}'
    ensure_directory_exists(directory)

    with open(f'{directory}/{perpage}_{pageno}_modified_file_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'file_path',
            'issue_id',
            'changes',
            'deletions',
            'additions',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for issue_data in issues_data:
            writer.writerow(issue_data)

def write_label_to_csv(issues_data, owner, repo, perpage, pageno):
    directory = f'{owner}/{repo}'
    ensure_directory_exists(directory)

    with open(f'{directory}/{perpage}_{pageno}_label_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "id",
            "node_id",
            "url",
            "name",
            "color",
            "default",
            "description",
            "issue_id"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for issue_data in issues_data:
            writer.writerow(issue_data)
