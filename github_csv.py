"""Read and commit UTF-8 files through GitHub's repository contents API."""

import base64
from urllib.parse import quote

import requests


class GitHubCSV:
    def __init__(self, token, repository, branch, path="docs/PAXCostAnalysis.csv"):
        if not all((token, repository, branch)):
            raise ValueError("Set GITHUB_TOKEN, GITHUB_REPOSITORY and GITHUB_BRANCH together.")
        self.branch = branch
        self.file_label = "CSV" if path.endswith(".csv") else path
        self.url = (
            f"https://api.github.com/repos/{quote(repository, safe='/')}"
            f"/contents/{quote(path, safe='/')}"
        )
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _check_response(self, response):
        if response.status_code == 409:
            raise RuntimeError(f"The {self.file_label} changed on GitHub. Please retry your change.")
        if not response.ok:
            raise RuntimeError(
                f"GitHub {self.file_label} request failed (HTTP {response.status_code}). "
                "Check the repository, branch, token permissions and branch protection."
            )

    def read(self):
        try:
            response = requests.get(
                self.url, headers=self.headers, params={"ref": self.branch}, timeout=30
            )
        except requests.RequestException:
            raise RuntimeError(f"Unable to read the {self.file_label} from GitHub. Please try again.") from None
        self._check_response(response)
        data = response.json()
        if data.get("encoding") != "base64":
            raise RuntimeError(f"GitHub did not return the {self.file_label} contents in the expected format.")
        return base64.b64decode(data["content"]).decode("utf-8-sig"), data["sha"]

    def write(self, content, sha, message):
        try:
            response = requests.put(
                self.url,
                headers=self.headers,
                json={
                    "message": message,
                    "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
                    "sha": sha,
                    "branch": self.branch,
                },
                timeout=30,
            )
        except requests.RequestException:
            raise RuntimeError(
                f"Could not confirm the GitHub save. Check the {self.file_label} on GitHub before retrying."
            ) from None
        self._check_response(response)
        return response.json()["content"]["sha"]
