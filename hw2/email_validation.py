import re


def fun(s: str) -> bool:
    if s.count('@') != 1:
        return False
    username, domain = s.split('@')
    if domain.count('.') != 1:
        return False
    sitename, extension = domain.split('.')

    username_pattern = r'^[a-zA-Z0-9_-]+$'
    if not re.match(username_pattern, username):
        return False

    sitename_pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(sitename_pattern, sitename):
        return False

    extension_pattern = r'^[a-zA-Z]+$'
    if not re.match(extension_pattern, extension):
        return False

    if len(extension) > 3:
        return False

    return True


def filter_mail(emails):
    return list(filter(fun, emails))


if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)
