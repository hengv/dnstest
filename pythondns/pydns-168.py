import dns.resolver,time

dnsserver='168.63.129.16'
while True:
    try:
        a=dns.resolver.get_default_resolver()
        dns.resolver.default_resolver.nameservers=[dnsserver]
        b=a.query('kuaishou.com','a')
        querytime = b.response.time
        address = b[0].address
        usingtime = time.ctime()
        print_text = str(querytime) + ' '+ usingtime + ' ' + address + ' ' + '\n'
    except Exception as e:
        print_text='8888 '+time.ctime()+' dns '+dnsserver+' failed test record: type '+ qtype +' query '+e.__class__.__name__+' '+ str(e)+'\n'
    
    with open("pydns-168.63.129.16.log",'a') as f:
        # print(print_text)
        f.write(print_text)
    
    time.sleep(60)
