from get_emails_github import *

def olderCommitPage(page_tree):
    try:
        sel = CSSSelector(".pagination")
        return sel(page_tree)[0][1].get("href")
    except Exception as e:
        return None

def newerCommitPage(page_tree):
    try:
        sel = CSSSelector(".pagination")
        return sel(page_tree)[0][0].get("href")
    except Exception as e:
        return None

def getCommits(user_project_name):
    # total_commits = getTotalCommits(user_project_name)
    url = "https://github.com/" + user_project_name + "/commits/master"
    print(url)
    commit_links = []
    num_pages = 100
    for _ in range(num_pages):
        r = requests.get(url)
        tree = html.fromstring(r.text)
        sel = CSSSelector("p.commit-title a.message")
        commit_links += [commit_href.get('href') for commit_href in sel(tree)]
        url = olderCommitPage(tree)
        print(url)
        if not url:
            break
    with open("commit_data/"+user_project_name.replace("/","_")+"_commit_links.dat", "a+") as cf:
        for each_link in commit_links:
            cf.write(each_link+"\n")
    return commit_links

def getCommitMetadata(link):
    r = requests.get(link)
    tree = html.fromstring(r.text)

    commit_date_sel = CSSSelector(".commit-meta relative-time")
    commit_date = commit_date_sel(tree)[0].get("datetime")

    changed_filename_sel = CSSSelector("div.file-info a.link-gray-dark")
    changed_filenames = [ele.text for ele in changed_filename_sel(tree)]

    return (link, commit_date, changed_filenames)

def main(choices):
    try:
        for project_name in choices:
            cf_processed = open("commit_data/"+project_name.replace("/","_")+"_commit_links_processed.dat", "a+")
            commits = getCommits(project_name.strip())
            print("Scraping Metadata for "+str(len(commits))+" commits")
            for commit_href in commits:
                print(commit_href)
                (commit_link, commit_date, changed_filenames) = getCommitMetadata("https://github.com"+commit_href)
                cf_processed.write(commit_link+"|"+commit_date+"|"+str(changed_filenames)+"\n")
            cf_processed.close()
    except Exception as e:
        print(str(e))
        raise e

if __name__ == "__main__":
    try:
        from sys import argv
        project_names_filename = argv[1]
        choices = []

        while True:
            choices = chooseRepos(project_names_filename, 1)
            main(choices)

    except EOFError:
        print("Finished")

    except:
        patchUnfinished(project_names_filename, choices)
        print("Handled Patch Unfinished")
