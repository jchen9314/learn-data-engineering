# Linux Command

- `sudo`: SuperUser DO, useful to access restricted files and operations

- `curl`
  - transfer data to or from a server, using any of the supported protocols (HTTP, FTP, IMAP, POP3, SCP, SFTP, SMTP, TFTP, TELNET, LDAP, or FILE).
  - can transfer multiple files at once
  
  ```shell
  curl [options] [URL...]
  ```

  - `curl -sSL`:
    - `-s` = `--silent`:  do not show progress meter or error messages
    - `-S` = `--show-error`: show an error message if it fails
    - `-L` = `--Location`: If the server reports that the requested page has moved to a different location (indicated with a Location: header and a 3XX response code), this option will make curl redo the request on the new place

- `mkdir`
  - `-p`: mkdir -p command you can create sub-directories of a directory

- `echo`: print the parameters passed to it

- dollar sign `$` (Variable): \$ before the parenthesis usually refers to a variable

- parenthesis `()`: command substitution

- `chmod +x` file_name: make the file executable

- `tar -xzf`: unzip gzipped file
  - x: extract (`--extract`, `--get`)
  - z: gzipped archive (`--gzip`)
  - f: get from a file (`--file`, `-F`)
