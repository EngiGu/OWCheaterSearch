import socket


def dns_resolver(domain):  # 获取域名解析出的IP列表
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        # print(str(e))
        pass
    if not ip_list:
        return 'null'
    return ip_list.pop(0)


if __name__ == "__main__":
    print(dns_resolver('mvl.sofoko.club'))
