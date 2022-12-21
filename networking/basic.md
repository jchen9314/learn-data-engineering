# Networking 101

## IP address (IPv4)

It can be represented by 4 decimal numbers or binary numbers, separated by periods

- in binary form, each number has mostly 8 digits
- each number is called octet
- in total, ipv4 address is 32 bits long, each number can be between 0 and 255

## CIDR Notation

- classless inter domain routing: can use variable number of bits at the beginning of an IP to represent the network portion; cidr tells you how many bits you are using to define the network portion
  - for example, `/16` means using first 16 bits to represent the network, and the remaning 16 bits to represent the host.

## Public and Private IP

- Private
  - IP address used on local network
  - Cannot be used on the Internet
  - Must be in approved range
  - Can be reused in separate private networks
- Public
  - can be used on the Internet
  - glocally unique
  - must be purchased/leased
  - used by public-facing cloud services
- Private IP Ranges
  - 10.0.0.0/8: 16M addresses
  - 172.16.0.0/12: 1M addresses
  - 192.168.0.0/16: 65K addresses