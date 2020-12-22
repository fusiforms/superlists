<!-- cSpell:ignore mkdbuttons, nsdname, ostc -->
<!-- cSpell:words Elspeth, vnet, nics, mkdir,  -->
<!-- cSpell:enableCompoundWords -->

# Brief instructions for how to get a Linux VM server running on Azure

To run the Django superlists web app described in _Test-Driven Development with Python_

Anthony Montague _20 December 2020_

## Set up an account in Azure and login

Create a free account at [portal.azure.com](https://portal.azure.com/)

Install the Azure CLI and check the installation was successful.
It is worth installing the Azure Tools extension for VS Code to provide tighter integration.

```bash
brew install azure-cli
az --version
```

Login to the Azure account using:

```bash
az login
```

This will open a web browser and ask for your credentials. On successful login, the shell
will show your subscription information in JSON.
A list of all subscriptions can be obtained using:

```bash
az account list --output table
```

If you have set up a free account, it's likely that there is only one subscription
and that it's name is `Free Trial`. For paid subscriptions the names will be different.
Make a note of the subscription name.
In my case the subscription is `Fusiforms Subscription`

## Set up a resource group

At this point we need to choose a location for our services.
Really, anything will do, but if you do want to choose something local, the output from the three commands below
will be helpful.
In my case, I want to find a location in Australia.
The first query lists all possible locations matching our search parameter. The first column in the table gives
the name for use in future Azure commands.
The second query gives us the physical locations, in case they aren't clear from the names.
The third query identifies locations that offer free appservice services - this may be useful for future
exploration, so ideally pick one of these.

```bash
az account list-locations --output table --query "[?contains(@.regionalDisplayName, 'Australia')==\`true\`]"
az account list-locations --output table --query "[?contains(@.regionalDisplayName, 'Australia')==\`true\`].{name:name, location:metadata.physicalLocation}"
az appservice list-locations --sku FREE --output table --query "[?contains(@.name, 'Australia')==\`true\`]"
```

In my case the best option is `australiasoutheast`

Create a resource group, giving it a helpful name (I'm using the name `rg-superlists`) and using the location just decided.
Configure the Azure CLI to use this group for future commands.
(Note the `az configure` command writes to the file `~/.azure/config`)

```bash
az group create --name rg-superlists --location australiasoutheast
az configure --defaults group=rg-superlists
```

## Start with some virtual networking

An Azure VM cannot easily be changed between virtual networks (vnet)s once it has
been set up, so it's better to set up the networking first.

We'll be setting up a virtual network with one subnet (front-end - for our internet facing
web-server). The VM will have a network interface that connects to the internet using
a network security group to manage the allowed connections.

We will also set up a DNS zone and a record in the DNS zone that points to the public IP address
on our network interface. The IP address is dynamic and changes when the VM is restarted - Azure
handles this by using a named IP address resource.

There is a security risk in our setup: the SSH port on the VM is open to the whole internet.
We can fix this by using a VPN, which we might do later...

### Create a virtual network with a front-end subnet

We do not need subnets initially, but it's helpful to set up a front end (internet-facing)
subnet now in case we want to add a backend (e.g. for a database) later

```bash
az network vnet create \
  --name vnet-superlists \
  --address-prefix 10.0.0.0/16 \
  --subnet-name sn-frontend \
  --subnet-prefix 10.0.1.0/24
```

### Create a network security group for the front-end subnet

```bash
az network nsg create \
  --name nsg-frontend
```

### Create network security group rules to allow HTTP, HTTPS and SSH traffic from the internet to the front-end subnet

```bash
az network nsg rule create \
  --nsg-name nsg-frontend \
  --name Allow-HTTP-All \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 100 \
  --source-address-prefix Internet \
  --source-port-range "*" \
  --destination-address-prefix "*" \
  --destination-port-range 80 443

az network nsg rule create \
  --nsg-name nsg-frontend \
  --name Allow-SSH-All \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 300 \
  --source-address-prefix Internet \
  --source-port-range "*" \
  --destination-address-prefix "*" \
  --destination-port-range 22
```

### Associate the front-end network security group to the front-end subnet

```bash
az network vnet subnet update \
  --vnet-name vnet-superlists \
  --name sn-frontend \
  --network-security-group nsg-frontend
```

### Create a public IP address to use for the superlists web server VM

```bash
az network public-ip create \
  --name ip-superlists-web
```

### Create a network interface for the superlists web server VM

```bash
az network nic create \
  --name nic-superlists-web \
  --vnet-name vnet-superlists \
  --subnet sn-frontend \
  --network-security-group nsg-frontend \
  --public-ip-address ip-superlists-web
```

### Create a DNS zone for our main website zone

You must have a domain name available to test with that you can host in Azure DNS.
You must have full control of this domain.
Full control includes the ability to set the name server (NS) records for the domain.

Create an Azure DNS zone using your parent domain.

```bash
az network dns zone create \
  --name fusiforms.com
```

Before you can delegate your DNS zone to Azure DNS, you need to know the name servers
for your newly created zone.
Azure DNS allocates name servers from a pool each time a zone is created.

```bash
az network dns record-set ns show \
  --zone fusiforms.com \
  --name @ \
  --query nsRecords[].nsdname \
  --output table
```

Now, login to the web management portal for your chosen domain name registrar
and update the name servers to be at least the first two listed in the response
(ideally all four).

After you complete the delegation, you can verify that it's working by using a
tool such as `dig` to query the Start of Authority (SOA) record for your zone.
The SOA record is automatically created when the zone is created.
You might need to wait 10 minutes or more after you complete the delegation,
before you can successfully verify that it's working.
It can take a while for changes to propagate through the DNS system.
You don't have to specify the Azure DNS name servers.
If the delegation is set up correctly, the normal DNS resolution process finds
the name servers automatically.

```bash
dig fusiforms.com SOA +short
```

The `dig` command should return a message containing one of the name servers you
just entered.

### Add an A record to the DNS

We want to add an A record to the DNS zone to point `www.fusiforms.com` to point
to the (dynamic) IP address of our front-end web server.
This needs to be an *'alias'* A record, which is created by using the `--target-resource`
parameter of the `az network dns record-set a create` command.

The `--target-resource` parameter need the full ID of the public ip resource (`ip-superlists-web`),
not just it's name, so we need to extract and store this id.

```language
ipid=$(az network public-ip show --name ip-superlists-web --query id --output tsv)
az network dns record-set a create \
  --name www \
  --zone-name fusiforms.com \
  --target-resource $ipid
```

## Generate an SSH key

If you've never created one before, the command is

```bash
ssh-keygen
```

**NOTE** *If you're on Windows, you need to be using Git-Bash for `ssh-keygen`
and `ssh` to work. There's more info in the
[installation instructions chapter](http://www.obeythetestinggoat.com/book/pre-requisite-installations.html)*

Just accept all the defaults if you really want to just get started in a hurry,
and no passphrase.

Later on, you'll want to re-create a key with a passphrase for extra security,
but that means you have to figure out how to save that passphrase in such a way
that Fabric won't ask for it later, and I don't have time to write instructions
for that now!

Make a note of your "public key"

```bash
cat ~/.ssh/id_rsa.pub
```

More info on public key authentication [here](https://www.linode.com/docs/networking/ssh/use-public-key-authentication-with-ssh/)

## Create a Web Server Virtual Machine

We need to find the name for the size of VM we want to create.
We'll use 'B1s' as that is free for the first year.

```bash
az vm list-sizes \
  --location australiasoutheast \
  --output table \
  --query "[?contains(@.name, 'B1s')==\`true\`]"
```

The query returns `Standard_B1s`.

We now have everything we need to create out virtual machine.

```bash
az vm create \
  --name vm-superlists \
  --nics nic-superlists-web \
  --image UbuntuLTS \
  --size Standard_B1s \
  --admin-username anthony \
  --ssh-key-values ~/.ssh/id_rsa.pub
```

## Log in for the first time

```bash
ssh anthony@www.fusiforms.com
```

It should just magically find your SSH key and log you in without any
need for a password.
SSH will ask if you wish to add your website to the list of know hosts, answer *yes*.

## Create another user for the VM

Note: the user that Azure creates using the details provided when creating the VM is not _root_
but an additional user with the ability to `su`.
Neither _root_ nor this user has a password.
For convenience, we will create an additional user with both SSH access and a password.

Our user will be called *elspeth*, have a home folder, use *bash* as her default shell.
Elspeth will be able to `sudo`.

```bash
sudo useradd --create-home --shell /bin/bash --groups sudo elspeth
sudo passwd elspeth
su - elspeth # switch-user to being elspeth!
```

## Add your public key to Elspeth

Copy your public key to your clipboard, and then

```bash
# As user elspeth
mkdir -p ~/.ssh
echo 'PASTE
YOUR
PUBLIC
KEY
HERE' >> ~/.ssh/authorized_keys
```

Now verify you can SSH in as Elspeth

```bash
# Exit twice to logout as both Elspeth and your initial user
# On the local terminal:
ssh elspeth@www.fusiforms.com
```

Also check you can use "sudo" as elspeth

```bash
sudo echo hi
```

## Appendix A: Another way to create an additional user for the VM

1. Copy your public key to your clipboard
2. Create a new user JSON file, and save it in the azure sub-directory as we do not
   want it in the repository as it contains security details. e.g. `azure/create_elspeth.json`.
   The JSON file contains the username, password, and the SSH public key we just copied.

   ```json
   {
     "username":"elspeth",
     "ssh_key":"PASTE YOUR PUBLIC
       KEY HERE",
     "password":"PASSWORD"
   }
   ```

3. Use the azure CLI to create the user from the JSON file (local):

   ```bash
   az vm extension set \
     --vm-name vm-superlists \
     --name VMAccessForLinux \
     --publisher Microsoft.OSTCExtensions \
     --version 1.4 \
     --protected-settings azure/create_elspeth.json
   ```

4. Test that the new user can connect over SSH and use `sudo` as above.
