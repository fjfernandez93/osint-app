import re, ipaddress


def detect_ip(text):

    pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    ip_list = list()

    matches = re.finditer(pattern, text)
    for match in matches:
        if match.group(0) not in ip_list:
            try:
                if ipaddress.ip_address(match.group(0)).is_private():
                    ip_list.append(match.group(0))
            except ValueError as err:
                pass
    return ip_list


def detect_email(text):
    # pattern = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    pattern = r"[a-zA-Z0-9.!#$%&['*+/=?^_`{|}~-]+@(?:[a-zA-Z0-9])?(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]+"
    email_list = list()
    matches = re.finditer(pattern, text)
    for match in matches:
        if match.group(0) not in email_list:
            email_list.append(match.group(0))
    return email_list