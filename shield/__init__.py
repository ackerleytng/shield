import sys
import shield_os
import shield_io
import shield_builtin


HOOK_MODULES = [shield_builtin, shield_os]


def do_hook(module):
    prefix = module.PREFIX
    hooks = module.HOOKS
    original_module = module.ORIGINAL_MODULE
    for hook in hooks:
        # Get the replacement function
        replacement_function = getattr(module, prefix + hook)
        # Store the original function
        module.HOOKS[hook] = getattr(original_module, hook)
        # Hook the function
        setattr(original_module, hook, replacement_function)


def do_unhook(module):
    hooks = module.HOOKS
    original_module = module.ORIGINAL_MODULE
    for hook in hooks:
        # Get the original function
        original_function = hooks[hook]
        # Unhook the function
        setattr(original_module, hook, original_function)
        # Reset saved hook
        module.HOOKS[hook] = None


def install_hooks():
    [do_hook(m) for m in HOOK_MODULES]


def uninstall_hooks():
    [do_unhook(m) for m in HOOK_MODULES]


# Need to add this in so that we don't hook in pytest
# If we want to hook in pytest, we can do that manually
if not hasattr(sys, "_called_from_test"):
    install_hooks()
