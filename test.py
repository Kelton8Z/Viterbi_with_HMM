import sys
def trY(S,T,count=0,limit=0,minCount=sys.maxsize):
    if S==T:
        if limit==-1:return 0
        else:
            return 1
    limit += 1
    count += 1
    assert(limit<len(S))
    for i in range(len(S)-1):
        cur = S[:i] + S[i+1:] + S[i]
#        assert(S!=cur)
        try:
            count += trY(cur,T,count,limit,minCount)
            minCount = min(count,minCount)
        except:
            count = 0
            continue
    res = minCount if limit==0 else count
    return res

assert(trY("k","k",-1,-1)==0)
assert(trY("ak","ka",-1,-1)==1)
assert(trY("akc","cka",-1,-1,sys.maxsize)==2)
print(trY("acdk","ckad",-1,-1,sys.maxsize))
#assert(trY("acdk","ckad",-1,-1,sys.maxsize)==2)


print(trY("kjsabiv","kjsabvi",-1,-1,sys.maxsize))
