# 由 asr.json 出「已校正」逐字時間（每個中文字一粒）
import json,re
FIX={('精',10.78):'症',('臟',11.16):'狀',('功',8.04):'供',('瘦',31.86):'收',('臟',30.02):'律',('速',70.16):'促',('心',77.70):'新',('臟',78.08):'陳'}
DEL={('過',40.64),('回',35.12),('睡',12.70),('覺',12.96)}
def chars(asr):
    out=[]
    for seg in json.load(open(asr)):
        for w in seg['words']:
            t=re.sub(r'[，。、,.!?？！\s]','',w['w'])
            parts=list(t)
            n=max(len(parts),1); d=(w['e']-w['s'])/n
            for k,c in enumerate(parts):
                s=round(w['s']+k*d,2); e=round(w['s']+(k+1)*d,2)
                key=(c,round(w['s'],2)) if n==1 else (c,s)
                if (c,round(s,2)) in DEL or key in DEL: continue
                c=FIX.get((c,round(s,2)),FIX.get(key,c))
                out.append({'c':c,'s':s,'e':e})
    return out
if __name__=='__main__':
    cs=chars('asr.json'); json.dump(cs,open('chars.json','w'),ensure_ascii=False)
    print(''.join(c['c'] for c in cs))
