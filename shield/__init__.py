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


do_hook(shield_builtin)
shield_io.do_hook()
shield_os.do_hook()
