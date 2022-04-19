# odoo-ce-inventory
This repository stores hosts informations and related variables for this specific instance of Odoo.
## Requirements

1. Clone this repo and [odoo-provisioning](https://gitlab.com/coopdevs/odoo-provisioning) in the same directory

2. If you want to test this set up locally, install [devenv](https://github.com/coopdevs/devenv/) and do:
   ```sh
   cd odoo-ce-inventory
   devenv # this creates the lxc container and sets its hostname
   ```
3. Go to `odoo-provisioning` directory and install its Ansible dependencies:
   ```sh
   cd ../odoo-provisioning/
   ansible-galaxy install -r requirements.yml
   ```
4. Execute playbook sys_admins to create users
   * development local mode
    ```sh
    ansible-playbook playbooks/sys_admins.yml -i ../odoo-ce-inventory/inventory/hosts --limit=dev --user=root
    ```
   * testing mode
    ```sh
    # In testing, add param '-k' to force ansible to ask for the root password
    # You will need ssh root enabled and package 'sshpass' installed in your machine
    ansible-playbook playbooks/sys_admins.yml -i ../odoo-ce-inventory/inventory/hosts --limit=testing --user=root -k
    ```
5. Run `ansible-playbook` command pointing to the `inventory/hosts` file of this repository:
   * development local mode
   ```sh
   # tell it to keep it local with limit=dev
   # don't ask for vault pass as no secrets are required for local setups
   ansible-playbook playbooks/provision.yml -i ../odoo-ce/inventory/hosts --limit=dev
   ```
   * testing mode
   ```sh
   ansible-playbook playbooks/provision.yml -i ../odoo-ce/inventory/hosts --ask-vault-pass --limit=testing
   ```
   * production mode
   ```sh
   ansible-playbook playbooks/provision.yml -i ../odoo-ce/inventory/hosts --ask-vault-pass --limit=production
   ```
6. Start Odoo
   * development local mode
   ```sh
   sudo su - odoo
   cd /opt/odoo
   pyenv activate odoo
   ./odoo-bin -c /etc/odoo/odoo.conf -d odoo
   ```
7. Now, you can visit:
   * In development http://odoo-ce-singulars.local:8069
   * In testing http://lux.somenergia.lan:8069
   * In production http://ce-singulars.coopedevs.org
