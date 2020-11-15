
library(data.table)
library(dplyr)
library(lubridate)

commits_file <- "/home/local/SAIL/benjamin/dev/greenkeeper/csv/greenkeeper_commits.csv"
comments_file <- "/home/local/SAIL/benjamin/dev/greenkeeper/csv/greenkeeper_comments.csv"
events_file <- "/home/local/SAIL/benjamin/dev/greenkeeper/csv/greenkeeper_events.csv"
issues_file <- "/home/local/SAIL/benjamin/dev/greenkeeper/csv/greenkeeper_issues.csv"
pack_names_file <- "/home/local/SAIL/benjamin/dev/greenkeeper/csv/greenkeeper_package_names.csv"

commits <- fread(commits_file, nThread=20)
comments <- fread(comments_file, nThread=20)
events <- fread(events_file, nThread=20)
issues <- fread(issues_file, nThread=20)
package_names <- fread(pack_names_file, nThread=20)

# issues[, issue_id := 
#         str_match(issue_repo_url,
#                    "^https://api.github.com/repos/(.*?)$")[,2]
#         ]

#package_names[, package_id := 
#                str_match(package_gh_url,
#                          "^https://github\\.com/(.*?)/$")[,2]]


split_semver <- function(v) {
  return (unlist(strsplit(v, "\\.")))
}

major_versions_are_different <- function(old_v, new_v) {
  return (as.numeric(split_semver(new_v)[1]) > as.numeric(split_semver(old_v)[1]))
}

minor_versions_are_different <- function(old_v, new_v) {
  return (as.numeric(split_semver(new_v)[2]) > as.numeric(split_semver(old_v)[2]))
}

patch_versions_are_different <- function(old_v, new_v) {
  return (as.numeric(split_semver(new_v)[3]) > as.numeric(split_semver(old_v)[3]))
}

get_update_type <- function(row) {
  curr_v <- row['issue_dependency_actual_version']
  next_v <- row['issue_dependency_next_version']
  if (major_versions_are_different(curr_v, next_v)) {
    return("major")
  } else if (minor_versions_are_different(curr_v, next_v)) {
    return("minor")
  } else {
    return("patch")
  }
}


issues$issue_state <- factor(issues$issue_state)

gki <- 
  issues[issue_user_login == "greenkeeper[bot]"]
null_values <- 
  c("", "undefined")
gki_with_dependency <- 
  gki[!(issue_dependency_name %in% null_values) & !(issue_dependency_actual_version %in% null_values) & !(issue_dependency_next_version %in% null_values)]

gki_with_dependency$update_type <- apply(gki_with_dependency, 1, get_update_type)
gki_with_dependency$update_type <- factor(gki_with_dependency$update_type)

