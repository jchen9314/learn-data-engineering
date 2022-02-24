# SSH

## What is it

- secure shell networking protocol
- secure connection between two machines
- allow secure administration of servers
- use to transfer file to remote servers
- use to remote access/login to VMs

## How to use

- ssh client:
  - Linux and Mac user have ssh client already installed
  - Windows user needs to use unix-command prompt like Git bash or PuTTy
- make the connection
  - ssh username@serverhost
    - serverhost: IP address, domain name
  - authenticate yourself to the remote server through either one:
    - password
    - key

## SSH to Google VM

1. create a `.ssh` folder (if you don't have it) in the root directory of your machine
2. [generate a ssh key pair](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

   `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USER -b 2048`

   - replace `KEY_FILENAME` and `USER` with your information

   ssh-keygen saves your private key file to `~/.ssh/KEY_FILENAME` and your public key file to `~/.ssh/KEY_FILENAME.pub`.

3. put public key to GCP Cloud Engine: `Compute Engine` -> `Settings` -> `Metadata` -> `SSH KEYS` -> `ADD SSH KEY` -> `SAVE`
4. create a GCP VM instance: `GCP home page` -> `Compute Engine` -> `VM instances` -> `CREATE INSTANCE`
5. after the instance is running, copy the `EXTERNAL_IP`
6. run command to connect to VM: `ssh -i ~/.ssh/KEY_FILENAME USER@EXECUTER_IP`
7. if you don't want to run the command above, create a `config` file under `~/.ssh/` directory, and then run `ssh de-zoomcamp` to connect to the VM

   ```shell
   Host: ANY_NAME (eg. de-zoopcamp)
       HostName: EXTERNAL_IP (eg. 104.199.105.130)
       User: USER 
       IdentifyFile: ~/.ssh/gcp 
   ```

8. configure VS code to access VM

   - install extention: `Remote - SSH`
   - click `Remote Status bar` and `Remote - SSH: Connect to Host`

   ![remote-status-bar](https://code.visualstudio.com/assets/docs/remote/ssh-tutorial/remote-status-bar.png)

   ![remote-ssh-commands](https://code.visualstudio.com/assets/docs/remote/ssh-tutorial/remote-ssh-commands.png)

   - select the name of the `HOST` we configured earlier and a new window will pop up

## Reference

1. [ssh intro](https://www.youtube.com/watch?v=v45p_kJV9i4&ab_channel=JuniorDeveloperCentral)
2. [vs code remote-ssh setup](https://code.visualstudio.com/docs/remote/ssh-tutorial)
3. [de zoomcamp 1.4.1](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12&ab_channel=DataTalksClub)
