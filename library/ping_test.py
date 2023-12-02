#!/usr/bin/python

from ansible.module_utils.basic import *
import requests


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        sites=dict(type="list", required=True),
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
    result = dict(
        changed=False,
        status=[],
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # Pull argument from passed-in params
    sites = module.params["sites"]

    # Perform any pre-checks on our arguments
    if len(sites) < 0:
        module.fail_json(msg="Please pass at least 1 site", **result)

    status = []

    # Perform our logic
    for site in sites:
        _response = requests.get(site)
        _dict = {"site": site, "status": "UP" if _response.ok else "DOWN"}
        status.append(_dict)

    # Update our state
    result["status"] = status
    result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == "__main__":
    main()
