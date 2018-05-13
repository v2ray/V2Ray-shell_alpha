#!/usr/bin/env python3

from base64 import b64decode

def openGWFLIST(path):
    gwfList = []
    with open(path, "r") as f:
        gwflistBase64 = f.read()
        
        if gwflistBase64:
            for i in b64decode(gwflistBase64).decode("utf-8").split("\n"):
                # https://adblockplus.org/zh_CN/filters
                if i.startswith("!#"):
                    continue
                if i.startswith("!"): # remove Comments
                    continue
                if not i: # remove empty
                    continue
                if i.startswith("[AutoProxy"):
                    continue
                if i.startswith("@@"): # remove Exception rules
                    continue
                if i.startswith("!##############General List End#################"):
                    break
                else:
                    gwfList.append(i)
            del gwflistBase64
    return gwfList


if __name__ == "__main__":
  openGWFLIST("gfwlist.txt")
