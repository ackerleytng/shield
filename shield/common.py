def write_check(mode):
    # perhaps a check can be done here to allow writing in some places
    # i.e not totally no writing, but to only to allowed files
    # can be totally no writing for now
    if "w" in mode:
        print "No writing!"
