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


