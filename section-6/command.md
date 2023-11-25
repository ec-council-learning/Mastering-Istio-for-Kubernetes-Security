## Command used in this section

### Looping requests between namespaces

```
for from in "foo" "bar" "legacy"; do for to in "foo" "bar" "legacy"; do kubectl exec "$(kubectl get pod -l app=auth-test -n ${from} -o jsonpath={.items..metadata.name})" -c auth-test -n ${from} -- curl http://auth-test-service.${to}:80/headers -s -o /dev/null -w "${from} ---> ${to}: %{http_code}\n" -k; done; done
```

### To find IP address

`ifconfig`

### To enable TCPDUMP in istio-proxy

```
sudo tcpdump -vvvv -A -i eth0 '((dst port <port number> and net <IP address from the above command >))'
```

### Send request to legacy and foo service

```
curl http://auth-test-service.legacy/test -s -o /dev/null -w "%{http_code}" -k

curl http://auth-test-service.foo/test -s -o /dev/null -w "%{http_code}" -k

```

### Get `x-forwarded-client-cert` header

```
curl -s http://auth-test-service.foo/headers | jq .\"x-forwarded-client-cert\"

curl -s http://auth-test-service.legacy/headers | jq .\"x-forwarded-client-cert\"
```