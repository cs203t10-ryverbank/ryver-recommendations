import py_eureka_client.eureka_client as eureka_client

eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="ryver-recommendations",
                   instance_port=8084)

try:
    res = eureka_client.do_service("ryver-cms", "/")
    print(res, "is active")
except Exception:
    print("no cms service active")

while True:
    pass

