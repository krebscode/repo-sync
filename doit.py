#! /usr/bin/env python3
import pygit2
cfg = {
    "makefu-master": {
        "remote":  {
            "url" : "http://cgit.gum/stockholm.git"
            # optional, always use master
            # "ref" : "heads/master"
        },
        "mirror": {
            "url": "ssh://git@localhost:stockholm-mirror"
            # optional, use name as branch
            # "ref": "heads/lass-master"
        }
    }
}

pygit2.init_repository('lolgit', True)
repo = pygit2.Repository('lolgit')
for k,v in cfg.items():
    try: repo.remotes.delete(k)
    except KeyError: pass

    remote_refspec = "refs/" + v['remote']['ref'] if 'ref' in v['remote'] \
            else 'refs/heads/master'
    refspec = "+{}:refs/remotes/{}/master".format(remote_refspec,k)
    repo.remotes.create(k,v['remote']['url'],refspec)
    ret = repo.remotes[k].fetch()
    print(ret)
    # print(k,v)
