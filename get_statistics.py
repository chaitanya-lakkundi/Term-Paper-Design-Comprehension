def getCountDesignFilesCommits(filename):
    count_uml_xmi = 0
    commit_count = 0
    total_files = 0
    design_files_histogram = dict()
    with open(filename) as rf:
        data = rf.readlines()
        for each_commit in data:
            files_changed = eval(each_commit.split("|")[2])
            total_files += len(files_changed)
            design_files_changed = [filename for filename in files_changed if ".uml" in filename or ".xmi" in filename]
            for each_file in design_files_changed:
                design_files_histogram[each_file] = design_files_histogram.get(each_file, 0) + 1
            this_count_uml_xmi = len(design_files_changed)
            if this_count_uml_xmi:
                # print([filename for filename in files_changed if "uml" in filename or "xmi" in filename])
                pass
            this_commit_count = 1 if this_count_uml_xmi else 0

            count_uml_xmi += this_count_uml_xmi
            commit_count += this_commit_count

    return count_uml_xmi, commit_count, total_files

def getFirstCommitTime(filename):
    with open(filename) as rf:
        data = rf.readlines()
        for each_commit in data:
            pass

def getRevisionRatio(filename):
    i_commits = 0
    with open(filename) as rf:
        data = rf.readlines()
        total_commits = len(data)
        for each_commit in data:
            files_changed = eval(each_commit.split("|")[2])
            design_files_changed = [filename for filename in files_changed if ".uml" in filename or ".xmi" in filename]
            i_commits += 1 if len(design_files_changed) else 0
    revision_ratio = i_commits/total_commits
    return revision_ratio

def main(file_list):
    count_design_files = 0
    commit_count = 0
    total_files = 0
    avg_revision_ratio = 0
    for each_file in file_list:
        (this_count_design_files, this_commit_count, this_total_files) = getCountDesignFilesCommits(each_file)

        count_design_files += this_count_design_files
        commit_count += this_commit_count
        total_files += this_total_files
        try:
            avg_revision_ratio += getRevisionRatio(each_file)
        except:
            pass
    avg_revision_ratio /= len(file_list)

    print(total_files, count_design_files, commit_count, avg_revision_ratio)

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
