import sys
import shield_os
import shield_io
import shield_builtin


HOOK_MODULES = [shield_builtin, shield_os, shield_io]


def do_hook(module):
    prefix = module.PREFIX
    hooks = module.HOOKS
    original_module = module.ORIGINAL_MODULE
    for hook, info in hooks.iteritems():
        # Store the original function
        try:
            if info is None:
                original_function = getattr(original_module, hook)
            else:
                original_function = getattr(*info)
        except AttributeError as e:
            if "has no attribute" in e.message:
                # Different platforms will offer different hooks
                #   just ignore those that don't exist
                continue
            else:
                raise e

        # Get the replacement function
        replacement_function = getattr(module, prefix + hook)
        # Hook the function
        setattr(original_module, hook, replacement_function)
        # Store the original for unhooking
        module.ORIGINALS[hook] = original_function


def do_unhook(module):
    hooks = module.HOOKS
    originals = module.ORIGINALS
    original_module = module.ORIGINAL_MODULE
    for hook, info in hooks.iteritems():
        # Get the original function
        original_function = originals[hook]

        # Unhook the function
        if info is None:
            setattr(original_module, hook, original_function)
        else:
            module_, hook_ = info
            setattr(module_, hook_, original_function)


def install_hooks():
    [do_hook(m) for m in HOOK_MODULES]


def uninstall_hooks():
    [do_unhook(m) for m in HOOK_MODULES]


# Need to add this in so that we don't hook in pytest
# If we want to hook in pytest, we can do that manually
if not hasattr(sys, "_called_from_test"):
    install_hooks()
