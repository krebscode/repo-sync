#! /usr/bin/env python3
from git import Repo
import git

cfg = {
    "makefu": {
        "origin":  {
            "url" : "http://cgit.gum/stockholm"
            # optional, always use master
            # "ref" : "heads/master"
        },
        "mirror": {
            "url": "git@wolf:stockholm-mirror"
            # optional, use name as branch
            # "ref": "heads/lass-master"
        }
    },
    "tv": {
        "origin":  {
            "url" : "http://cgit.cd/stockholm"
        },
        "mirror": {
            "url": "git@wolf:stockholm-mirror"
        }
    }
#    "lassulus": {
#        "origin":  {
#            "url" : "http://cgit.cloudkrebs/stockholm"
#        },
#        "mirror": {
#            "url": "ssh://git@wolf:stockholm-mirror"
#        }
#    }
}


repo = Repo.init('lolgit',bare=True)
for k,v in cfg.items():
    # import pdb;pdb.set_trace()
    oname = k
    mname = oname+'-mirror'
    ourl = v['origin']['url']
    murl = v['mirror']['url']
    try: repo.delete_remote(oname)
    except git.exc.GitCommandError: pass

    try: repo.delete_remote(mname)
    except git.exc.GitCommandError: pass

    remote_ref = "refs/" + v['origin']['ref'] if 'ref' in v['origin'] \
            else 'refs/heads/master'
    local_ref = "refs/remotes/{}/master".format(oname)
    refspec = "+{}:{}".format(remote_ref,local_ref)
    oremote = repo.create_remote(oname,url=ourl)
    oremote.fetch(refspec=refspec)
    # finish fetching

    mremote = repo.create_remote(mname,murl)
    mirror_ref = "refs/heads/{}".format(oname)
    mrefspec = "{}:{}".format(local_ref,mirror_ref)
    push = mremote.push(refspec=mrefspec,force=True)

    # print(k,v)
