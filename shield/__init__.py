import sys
import shield_os
import shield_io
import shield_builtin


def do_hook(module):
    prefix = module.PREFIX
    hooks = module.HOOKS
    original_module = module.ORIGINAL_MODULE
    for hook in hooks:
        replacement_function = getattr(module, prefix + hook)
        setattr(original_module, hook, replacement_function)


def install_hooks():
    do_hook(shield_builtin)
    shield_io.do_hook()
    shield_os.do_hook()


# Need to add this in so that we don't hook in pytest
# If we want to hook in pytest, we can do that manually
if not hasattr(sys, "_called_from_test"):
    install_hooks()
