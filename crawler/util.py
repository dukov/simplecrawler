import string

def vid_gen(end, num_digits):
    digits = string.ascii_lowercase + string.ascii_uppercase + string.digits
    i = 0
    while i <= end:
        k = i
        res = []
        while True:
            res.append(digits[k%62])
            k = k/62
            if k == 0: break
        if num_digits > len(res):
            res+=[digits[0]]*(num_digits-len(res))
        yield i, list(reversed(res))
        i+=1
