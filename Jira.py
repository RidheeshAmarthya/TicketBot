import requests
import json
import config 

def get_jira_issue(jira_site, user_email, api_token, issue_key):
    """Retrieves a Jira issue and its description."""

    auth = (user_email, api_token)
    url = f"https://{jira_site}/rest/api/3/issue/{issue_key}"

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        issue_data = response.json()

        summary = issue_data["fields"]["summary"]
        description = issue_data["fields"].get("description")
        description_text = ""

        if description and description["content"]:
            for content_item in description["content"]:
                if content_item["type"] == "paragraph" and "content" in content_item:
                    for text_item in content_item["content"]:
                        if text_item["type"] == "text":
                            description_text += text_item["text"] + " "

        return summary, description_text.strip()

    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"
    except json.JSONDecodeError as e:
        return None, f"Error decoding JSON: {e}"
    except KeyError as e:
        return None, f"KeyError: {e}. Possible incorrect issue key or field name."

jira_site = "ridheesh.atlassian.net"
user_email = "vridheesh@gmail.com"
api_token = config.atlassian
issue_key = "MBA-7"  # Extract issue key from the URL

summary, description = get_jira_issue(jira_site, user_email, api_token, issue_key)

if summary:
    print(f"Summary: {summary}")
    print(f"Description: {description}")
else:
    print(description)



# Jira