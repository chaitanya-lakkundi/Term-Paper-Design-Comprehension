def getCountDesignFilesCommits(filename):
    count_uml_xmi = 0
    commit_count = 0
    with open(filename) as rf:
        data = rf.readlines()
        for each_commit in data:
            files_changed = eval(each_commit.split("|")[2])

            this_count_uml_xmi = len([filename for filename in files_changed if ".uml" in filename or ".xmi" in filename])
            if this_count_uml_xmi:
                # print([filename for filename in files_changed if "uml" in filename or "xmi" in filename])
                pass
            this_commit_count = 1 if this_count_uml_xmi else 0

            count_uml_xmi += this_count_uml_xmi
            commit_count += this_commit_count

    return count_uml_xmi, commit_count

def main(file_list):
    count_design_files = 0
    commit_count = 0
    for each_file in file_list:
        (this_count_design_files, this_commit_count) = getCountDesignFilesCommits(each_file)
        count_design_files += this_count_design_files
        commit_count += this_commit_count
    print(count_design_files, commit_count)

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
