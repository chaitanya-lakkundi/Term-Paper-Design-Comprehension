from get_emails_github import *

def forwardCommitPage(page_tree):
    try:
        sel = CSSSelector(".pagination")
        return sel(page_tree)[0][1].get("href")
    except Exception as e:
        return None

def getCommits(user_project_name):
    url = "https://github.com/" + user_project_name + "/commits/master"
    print(url)
    commit_links = []
    for _ in range(2):
        r = requests.get(url)
        tree = html.fromstring(r.text)
        sel = CSSSelector("p.commit-title a.message")
        commit_links += [commit_href.get('href') for commit_href in sel(tree)]
        url = forwardCommitPage(tree)
        if not url:
            break
    return commit_links

def getCommitMetadata(link):
    r = requests.get(link)
    tree = html.fromstring(r.text)

    commit_date_sel = CSSSelector(".commit-meta relative-time")
    commit_date = commit_date_sel(tree)[0].get("datetime")

    changed_filename_sel = CSSSelector("div.file-info a.link-gray-dark")
    changes_filenames = [ele.text for ele in changed_filename_sel(tree)]

    print(commit_date,changes_filenames)

def main(choices):
    try:
        for project_name in choices:
            commits = getCommits(project_name.strip())
            print("Scraping Metadata for "+str(len(commits))+" commits")
            for commit_href in commits:
                getCommitMetadata("https://github.com"+commit_href)
    except Exception as e:
        print(str(e))
        raise e

if __name__ == "__main__":
    try:
        from sys import argv
        username_list_filename = argv[1]
        choices = []

        while True:
            choices = chooseRepos(username_list_filename, 1)
            main(choices)

    except EOFError:
        print("Finished")

    except:
        patchUnfinished(username_list_filename, choices)
        print("Handled Patch Unfinished")
