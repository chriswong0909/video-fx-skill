import json
M=json.load(open('/home/claude/p/map.json'))
def f(t):
    for s,e,acc,d in M:
        if t<s: return round(acc/1.1,3)
        if t<=e: return round((acc+min(t-s,d))/1.1,3)
    return round((M[-1][2]+M[-1][3])/1.1,3)
