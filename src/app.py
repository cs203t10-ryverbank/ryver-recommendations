import py_eureka_client.eureka_client as eureka_client

eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="ryver-recommendations",
                   instance_port=8084)

res = eureka_client.do_service("ryver-cms", "/")
print(res)

while True:
    pass
