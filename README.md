# odoo-ce-inventory
This repository stores hosts informations and related variables for this specific instance of Odoo.
## Requirements

1. Clone this repo and [odoo-provisioning](https://git.coopdevs.org/coopdevs/odoo/odoo-provisioning/odoo-provisioning#requirements) in the same directory and install the environment requirements

2. Clone [odoo-ce](https://git.coopdevs.org/coopdevs/comunitats-energetiques/odoo-ce) in the same directory

3. If you want to test this set up locally, install [devenv](https://github.com/coopdevs/devenv/) and do:
   ```sh
   cd odoo-ce-inventory
   devenv # this creates the lxc container and sets its hostname
   ```
4. Go to `odoo-provisioning` directory and install its Ansible dependencies:
   ```sh
   cd ../odoo-provisioning/
   ansible-galaxy install -r requirements.yml
   ```
5. Execute playbook sys_admins to create users
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
6. Run `ansible-playbook` command pointing to the `inventory/hosts` file of this repository:
   * development local mode
   ```sh
   # tell it to keep it local with limit=dev
   # don't ask for vault pass as no secrets are required for local setups
   ansible-playbook playbooks/provision.yml -i ../odoo-ce-inventory/inventory/hosts --limit=dev
   ```
   * testing mode
   ```sh
   ansible-playbook playbooks/provision.yml -i ../odoo-ce-inventory/inventory/hosts --ask-vault-pass --limit=preprod
   ```
   * production mode
   ```sh
   ansible-playbook playbooks/provision.yml -i ../odoo-ce-inventory/inventory/hosts --ask-vault-pass --limit=prod
   ```
7. Start Odoo
   * development local mode
   ```sh
   # Make sure the lxc container is started
   sudo lxc-start odoo-ce
   ssh odoo@odoo-ce.local
   ```
   Inside the container
   ```sh
   cd /opt/odoo
   pyenv activate odoo
   ./odoo-bin -c /etc/odoo/odoo.conf -d odoo
   ```
8. Now, you can visit:
   * In development http://odoo-ce.local:8069
   * In testing http://erp-preprod.somcomunitats.coop
   * In production http://erp-prod.somcomunitats.coop

### Tips
You can skip the NGINX related task by adding `--skip-tags "nginx"` to the
`ansible-playbook` command.

You can run only the odoo-role task by adding `--tag odoo-role` to the `ansible-playbook` command.

