# This script is for educational purposes only.
# This script is not meant to be used for any malicious purpose including but not limited to:
# collecting personal information of users.
# for scraping GitHub for commercial purposes.
# for scraping GitHub for any other illegal purpose.

# The author of this script does not encourage nor will be responsible for such actions.

# It is important to read the GitHub terms and policies as it 
# may be against their terms to use this service for certain purposes.
# https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies#7-information-usage-restrictions

# Use this script at your own risk.


import requests
from bs4 import BeautifulSoup

# urls
root_url = "https://github.com"


class GithubUser:
    def __init__(self, username):
        self.name = None
        self.username = username
        self.profile_url = f"{root_url}/{username}"
        self.html = None
        self.soup = None
        self.following = []
        self.followers = []
        self.repos = []
        self.following_url = f"{root_url}/{username}?tab=following"
        self.followers_url = f"{root_url}/{username}?tab=followers"
        self.recent_30_repos_url = f"{root_url}/{username}?tab=repositories"

    def get_info(self):
        self.get_html(self.profile_url)
        self.name = self.soup.find(
            "span", {"class": "p-name vcard-fullname d-block overflow-hidden"}).text.strip()
        # self.bio = self.soup.find("div", {"class": "p-note user-profile-bio mb-3 js-user-profile-bio f4"}).text
        # self.location = self.soup.find("span", {"class": "p-label"}).text
        # self.company = self.soup.find("span", {"class": "p-org"}).text
        # self.website = self.soup.find("a", {"class": "u-url url"}).text
        # self.email = self.soup.find("a", {"class": "u-email"}).text
        # self.joined = self.soup.find("time-ago", {"class": "no-wrap"})["datetime"]
        # self.twitter = self.soup.find("a", {"class": "u-url url"})["href"]
        # self.avatar = self.soup.find("img", {"class": "avatar avatar-user width-full border color-bg-primary"})["src"]
        # self.followers_count = self.soup.find("span", {"class": "text-bold color-text-primary"}).text
        # self.following_count = self.soup.find("span", {"class": "text-bold color-text-primary"}).text
        # self.starred_count = self.soup.find("a", {"class": "js-selected-navigation-item HeaderNavlink px-0 py-3 border-top border-bottom"}).text
        # self.repos_count = self.soup.find("a", {"class": "js-selected-navigation-item HeaderNavlink px-0 py-3 border-top border-bottom"}).text

    def get_html(self, url):
        r = requests.get(url)
        self.html = r.text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_followers(self):
        self.get_html(self.followers_url)
        divs = self.soup.find_all(
            "div", {"class": "d-table-cell col-9 v-align-top pr-3"})
        for div in divs:
            github_username = div.find_all("span")[1].text
            self.followers.append(GithubUser(github_username))

    def get_following(self):
        self.get_html(self.following_url)
        divs = self.soup.find_all(
            "div", {"class": "d-table-cell col-9 v-align-top pr-3"})
        for div in divs:
            github_username = div.find_all("span")[1].text
            self.following.append(GithubUser(github_username))

    def get_repos(self, limit=30):
        self.get_html(self.recent_30_repos_url)
        div = self.soup.find("div", {"id": "user-repositories-list"})
        repos_list = div.find_all("li")[:limit]
        for repo in repos_list:
            repo_name = repo.find("a").text
            repo_url = repo.find("a")["href"]
            repo_desc = repo.find("p").text if repo.find("p") else None
            if repo.find("span", {"itemprop": "programmingLanguage"}):
                repo_lang = repo.find(
                    "span", {"itemprop": "programmingLanguage"}).text
            else:
                repo_lang = None
            # self.repos.append({
            #     "name": repo_name.strip(),
            #     "url": repo_url,
            #     "description": repo_desc.strip() if repo_desc else None,
            #     "language": repo_lang
            # })
            self.repos.append(GithubRepo(root_url + repo_url))

    def fetch_all(self):
        self.get_followers()
        self.get_following()
        self.get_repos()


class GithubRepo:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None
        self.name = None
        self.description = None
        self.language = None
        self.stars = None
        self.forks = None
        self.watchers = None
        self.contributors = []

    def get_html(self, url, write_to_file=False):
        r = requests.get(url)
        self.html = r.text
        # write html to file
        if write_to_file:
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(self.html)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def is_dot_env_file_present(self):
        self.get_html(self.url)
        files_div = self.soup.find("div", {"aria-labelledby": "files"})
        return files_div.text.find(".env") != -1

    def get_dot_env_file_content(self):
        self.get_html(self.url + "/blob/main/.env", write_to_file=True)
        env_lines = self.soup.find("table").find_all("tr")
        env_file_content = ""
        for line in env_lines:
            line_content = line.find_all("td")[1].text
            env_file_content += line_content + "\n"
        return env_file_content

    def get_info(self):
        self.get_html(self.url, write_to_file=True)
        self.name = self.soup.find(
            "strong", {"class": "mr-2 flex-self-stretch"}).text.strip()
        self.description = self.soup.find(
            "p", {"class": "f4 mb-3"}).text.strip()
        self.stars = self.soup.find(
            "svg", {"class": "octicon octicon-star mr-2"}).parent.find("strong").text.strip()
        self.forks = self.soup.find_all(
            "svg", {"class": "octicon octicon-repo-forked mr-2"})[1].parent.find("strong").text.strip()
        self.watchers = self.soup.find(
            "svg", {"class": "octicon octicon-eye mr-2"}).parent.find("strong").text.strip()


def main():
    username = input("Enter Github username: ")
    user = GithubUser(username)
    user.fetch_all()


if __name__ == "__main__":
    main()
