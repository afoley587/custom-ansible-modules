#!/usr/bin/python

from ansible.module_utils.basic import *
import math


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        radius=dict(type="float", required=True),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, area=0)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # Pull argument from passed-in params
    radius = module.params["radius"]

    # Perform any pre-checks on our arguments
    if radius < 0:
        module.fail_json(msg="radius cannot be less than 0", **result)

    # Perform our logic and update our state
    result["area"] = math.pi * radius * radius
    result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == "__main__":
    main()
