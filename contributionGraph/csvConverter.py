import csv


def write_issues_to_csv(issues_data):
    with open('my_issues_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        
        
        
def write_comment_to_csv(issues_data):
    with open('my_comment_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'issue_id',
            'id' ,
            'user'  ,
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




def write_modified_file_to_csv(issues_data):
    with open('my_comment_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
            
            
def write_label_to_csv(issues_data):
    with open('my_comment_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
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

