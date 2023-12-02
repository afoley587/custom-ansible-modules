# 1 Dollar DevOps: Writing Custom Ansible Modules With Python

![Thumbnail](./images/thumbnail.png)

Ansible is a powerful open-source automation tool that simplifies complex 
IT tasks, enabling users to define and manage infrastructure as code. 
Developed by Red Hat, Ansible is widely utilized for configuration management, 
application deployment, and task automation across a multitude of servers and systems. 
One of its key strengths lies in its agentless architecture, allowing users to control 
and orchestrate remote servers without the need for installing any additional software 
on target machines. Ansible employs a declarative language, YAML, for describing automation 
playbooks, making it highly readable and accessible for users at various skill levels. 
With its focus on simplicity and ease of use, Ansible has become a go-to solution for DevOps 
teams and system administrators seeking efficient, scalable, and consistent automation across 
their environments.

Ansible has a plethora of standard and included modules which can be found in their 
[documentation](https://docs.ansible.com/ansible/latest/module_plugin_guide/index.html), but
developers often extend its capabilities by writing custom modules in Python. 
These modules serve as the building blocks for executing specific tasks within playbooks, 
enhancing Ansible's flexibility and adaptability to diverse use cases. Whether it involves 
integrating with unique APIs, interacting with specialized hardware, or performing tailored 
configurations, creating custom modules empowers users to tailor Ansible to 
their specific needs, fostering a more seamless and comprehensive automation experience. This fusion of 
Ansible's simplicity and the extensibility provided by Python custom modules makes it a formidable tool 
for automating and managing diverse IT infrastructure scenarios.

## Getting Our Feet Wet

In this blog post, we will build out two custom modules to drive home the idea of how this works.
You'll notice similar structures and patterns in both modules that will expand to 
any other module you find yourself needing to make.

If you plan on following along with this blog post, please install
the requirements into your venv. They can be found [here](https://github.com/afoley587/custom-ansible-modules/blob/main/requirements.txt).

If you've used ansible before, you'll be aware that it has a custom directory
structure where it looks for specific items like variables, hosts, roles, etc.
It's no different with custom modules and we will need a `library` directory
at the root level of our project:

```shell
prompt> mkdir -p library/
```

This directory will house all of our python (`.py`) files which will
comprise our modules. Let's make two files for our two modules:

```shell
prompt> touch library/area_of_circle.py
prompt> touch library/ping_test.py
```

### Module 1: area_of_circle
And now we can begin to fill out our code. Let's start with the area
of a circle:

```python
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
```

Step 1: we need a shebang (`#!/usr/bin/python`) to set our python interpreter.

Step 2: we import the ansible libraries/modules with the following

```python
from ansible.module_utils.basic import *
```

Step 3: We need to define any input arguments, instantiate our module,
and then seed our results dictionary:

```python
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
```

We see that our module takes 1 input argument, `radius`, which is a float. The result
which gets returned to the ansible playbook will have 1 custom output, which is `area`.
We will see how to use that when we actually run our modules.

Step 4: Check for `check_mode` and do any input validation we want on the arguments.

```python
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
```

Step 5: Actually run the action and update our state.

```python
    # Perform our logic and update our state
    result["area"] = math.pi * radius * radius
    result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)
```

### Module 2: ping_test
Let's follow the same exact steps for the second module, ping_test:

```python
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
```

Step 1: We have our shebang at the top of the file :white-check:
Step 2: we import the ansible libraries/modules :white-check:
Step 3: We need to define any input arguments, instantiate our module,
and then seed our results dictionary :white-check:
Step 4: Check for `check_mode` and do any input validation we want on the arguments :white-check:
Step 5: Actually run the action and update our state :white-check:

Don't you love it when we have nicely defined patterns?

## Using The Modules
Now we have our two modules and they are in the `library/` directory. How do we use
them and their outputs?

Let's look at our `site.yml`:

```yaml
- name: Testing our custom module
  hosts: localhost
  gather_facts: true

  tasks:
    - name: Use Our Custom Module To Calculate The Area Of A Circle
      area_of_circle: 
        radius: 10
      register: area_of_circle_result
    
    - name: Show area of circle
      debug:
        msg: 
          - "The are of the circle is {{ area_of_circle_result.area }}!"

    - name: Use Our Other Custom Module To Ping Some Websites
      ping_test: 
        sites:
          - https://google.com
          - https://youtube.com
          - https://ebay.com
      register: ping_test_result

    - name: Show Ping Test Results
      debug:
        msg: 
          - "{{ item.status }}"
      with_items: "{{ ping_test_result.status }}"
      loop_control:
        label: "{{ item.site }}"
```

We see that we can call the modules just like we would call any other module. We
can store the result with `register`, and then we can use the specific output
fields we defined in the python:

```yaml
    - name: Use Our Custom Module To Calculate The Area Of A Circle
      area_of_circle: 
        radius: 10
      register: area_of_circle_result

    - name: Show area of circle
      debug:
        msg: 
          - "The are of the circle is {{ area_of_circle_result.area }}!"
```

Our ping tests returned a list of dictionaries. So we can loop through
that just as we would other yaml lists:

```yaml
    - name: Use Our Other Custom Module To Ping Some Websites
      ping_test: 
        sites:
          - https://google.com
          - https://youtube.com
          - https://ebay.com
      register: ping_test_result

    - name: Show Ping Test Results
      debug:
        msg: 
          - "{{ item.status }}"
      with_items: "{{ ping_test_result.status }}"
      loop_control:
        label: "{{ item.site }}"
```

We can run the entire thing and see our outputs:

```python
prompt> ansible-playbook site.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Testing our custom module] *****************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [localhost]

TASK [Use Our Custom Module To Calculate The Area Of A Circle] ***********************************************************************
changed: [localhost]

TASK [Show area of circle] ***********************************************************************************************************
ok: [localhost] => {
    "msg": [
        "The are of the circle is 314.1592653589793!"
    ]
}

TASK [Use Our Other Custom Module To Ping Some Websites] *****************************************************************************
changed: [localhost]

TASK [Show Ping Test Results] ********************************************************************************************************
ok: [localhost] => (item=https://google.com) => {
    "msg": [
        "UP"
    ]
}
ok: [localhost] => (item=https://youtube.com) => {
    "msg": [
        "UP"
    ]
}
ok: [localhost] => (item=https://ebay.com) => {
    "msg": [
        "UP"
    ]
}

PLAY RECAP ***************************************************************************************************************************
localhost                  : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

# References
* [Developing Ansible Modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
* [My GitHub Repo](https://github.com/afoley587/custom-ansible-modules)