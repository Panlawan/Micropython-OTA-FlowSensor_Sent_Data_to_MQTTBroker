import ujson
a = 50
b = 10

def make_config(a, b):
    return {'data': {'flow': a, "test": b}}

app_config = ujson.dumps(make_config(a, b))
#msg = ujson.dumps(app_config)

print(app_config)