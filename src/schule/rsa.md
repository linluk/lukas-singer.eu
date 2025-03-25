---
title: RSA Kryptosystem
lang: de
keywords:
- tfbs-eke
- informatik
- kryptographie
- rsa
- rivest, shamir adleman
- verschlüsselung
description: Info und Beispiel zum RSA-Kryptosystem für den Mathematikunterricht an der Tiroler Fachberufsschule für Elektrotechnik, Kommunikation und Elektronik
use-toc: false
nav-schule: true
nav-schule-rsa: true
---

Das *RSA-Kryptosystem* ist ist ein Asymmetrisches Verfahren in der Kryptographie.
Benannt ist RSA nach den drei Mathematikern Rivest, Shamir, Adleman.
Kryptosystem bedeutet, dass es sich nicht nur zur Verschlüsselung, sondern auch zur Validierung von Nachrichten eignet.
Asymmetrisches Verfahren bedeutet, dass es ein Schlüsselpaar, also zwei verschiedene Schlüssel gibt.
Man spricht von *public Key* (öffentlicher Schlüssel) und *private Key* (privater oder geheimer Schlüssel).
Wurde eine Nachricht mit einem Schlüssel eines Schlüsselpaares verschlüsselt, kann diese nur mit dem anderen Schlüssel des Schlüsselpaares entschlüsselt werden.

Mathematische Grundlagen
========================

Primzahlen
----------

$$
    \mathbb{P} := \{ p \in \mathbb{N} \text{ } | \text{ } p \bmod q \neq 0 \text{ } \forall \text{ } q \in \mathbb{N} \text{ } | \text{ } q > 1 \land q < p \}
$$

$$ \mathbb{P} = \{ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, \text{...} \} $$

**Sieb des Eratosthenes**

Eratosthenes von Kyrene war ein griechischer Gelehrter der ca. 200 vor Christus lebte.
Eratosthenes wurde vor allem dafür bekannt den Umfang der Erde, für die damalige Zeit, erstaunlich genau berechnet zu haben.
Eine weitere seiner Arbeiten beschäftigt sich damit, wie man eine Liste von Primzahlen generieren kann.

Dabei werden die Zahlen von 2 beginnend bis zu der höchsten Zahl die man betrachten möchte notiert.
Dann startet der Algorithmus.
Man nimmt die erste Zahl, die noch nicht gestrichen ist. Diese ist eine Primzahl!
Dann streicht man alle vielfachen dieser Zahl und beginnt wieder von vorne mit der nächsten nicht gestrichene Zahl usw.

~~~python
  def eratosthenes(n=100):
      e = set(range(2, n))
      p = 0
      while len(e) > 0:
          p = min(e)
          e.discard(p)
          for i in range(2, 1 + n // p):
              e.discard(p * i)
          yield p
  primes = list(eratosthenes(1000))
  print(primes[-10:])
~~~

~~~
 [937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
~~~

**Euklidischer und erweiterter euklidischer Algorithmus**

Der $ggT(a, b)$ (sprich: größter gemeinsamer Teiler von $a$ und $b$) ist die größte Zahl die sowohl $a$ als auch $b$ ohne Rest teilt.
Um den *ggT* zu ermitteln, kann man den *euklidischen Algorithmus* nutzen.
Der euklidische Algorithmus nutzt die Modulorechnung zur Ermittlung des ggT.
Zur Erinnerung der Rest $r$ erfüllt die Ganzzahlige Gleichung
$$ a = q \cdot b + r $$

Sucht man den $ggT(23, 17)$ trägt man $a$ und $b$ in folgende Tabelle ein und füllt die Zeile entsprechend der Gleichung aus.
Anschließend schreibt man das $b$ aus der vorherigen Zeile in die Spalte $a$ und das $r$ in die Spalte $b$.
Das wiederholt man so lange bis $r = 0$ ist.

<div class="tbl-borders tbl-padding">
|  a |  b |  q |  r |
|---:|---:|---:|---:|
| 23 | 17 |  1 |  6 |
| 17 |  6 |  2 |  5 |
|  6 |  5 |  1 |  1 |
|  5 |  1 |  5 | ***0*** |
</div>

Den *ggT* findet man dann in der vorletzten Zeile in Spalte $r$ (oder in der letzten in Spalte $b$).

Für das RSA-Verfahren benötigt man nicht nur den ggT alleine, sondern den ggT als Linearkombination in der Form:
$$ ggT(a, b) = a \cdot x + b \cdot y $$

Wobei $x$ und $y$ ganze Zahlen sein müssen, also $x, y \in \mathbb{Z}$.

Um $x$ und $y$ zu ermitteln könnte man nun probieren, aber für große Zahlen ist das nicht sehr effektiv.
Man nutzt den *erweiterten euklidischen Algorithmus*.

Beim erweiterte euklidische Algorithmus startet man gleich wie beim (einfachen) euklidischen Algorithmus und fügt der Tabelle noch zwei Spalten $x$ und $y$ hinzu.
Man arbeitet sich nachdem man den ggT ermittelt hat wieder von unten nach oben.

Als erstes trägt man in die unterste Zeile $x = 0$ und $y = 1$ ein.
Das erfüllt die Gleichung $ggT(a, b) = a \cdot x + b \cdot y$ für diese Zeile.

Die vorherige Spalte $y$ wird nun zur nächsten (darüberliegenden) Spalte $x$. Somit muss
man für diese Zeile nur noch $y$ so wählen, dass $ggT(a, b) = a \cdot x + b \cdot y$ stimmt.

Also Formel umstellen nach:
$$ y = \frac{ggT(a, b) - a \cdot x}{b} $$

<div class="tbl-borders tbl-padding">
|  a |  b | q | r |  x |  y |
|---:|---:|---:|---:|---:|---:|
| 23 | 17 | 1 | 6 |  *3* | *-4* |
| 17 |  6 | 2 | 5 | -1 |  3 |
|  6 |  5 | 1 | 1 |  1 | -1 |
|  5 |  1 | 5 | ***0*** |  0 |  1 |
</div>


Aus der Tabelle kann man jetzt folgendes Ablesen:
Der $ggT(a, b)$ mit $a = 23$ und $b = 17$ ist $1$.
Als Linearkombination gilt:
$$ ggT(23, 17) = 1 = 23 \cdot 3 + 17 \cdot - 4 $$

~~~python
  def euklid(a, b):
      i = 0
      a = {i: a}
      b = {i: b}
      r = {i: a[i] % b[i]}
      while r[i] != 0:
          i += 1
          a[i] = b[i - 1]
          b[i] = r[i - 1]
          r[i] = a[i] % b[i]
      g = b[i]
      x = {i: 0}
      y = {i: 1}
      while i > 0:
          i -= 1
          x[i] = y[i + 1]
          y[i] = (g - a[i] * x[i]) // b[i]
      return g, x[0], y[0]

  a, b = 23, 17
  ggT, x, y = euklid(a, b)
  print(f'ggT({a}, {b}) = {ggT} = {a} * {x} + {b} * {y}')
~~~

~~~
 ggT(23, 17) = 1 = 23 * 3 + 17 * -4
~~~

**Eulersche $\phi$-Funktion**

Die eulersche $\phi$-Funktion (Phi-Funktion) ist eine Zahlentheoretische Funktion.
$\phi(n)$ gibt an wieviele zu $n$ teilerfremde Zahlen es gibt.

Für Primzahlen gilt:
$$ \phi(p) = p − 1 \text{ mit } p \in \mathbb{P} $$
Für Produkte von Primzahlen (also jede beliebige natürliche Zahl größer als 1) gilt:
$$
 \phi(n) = \phi(p1 \cdot p2 \cdot ... \cdot pk ) = \phi(p1) \cdot \phi(p2 ) \cdot ... \cdot \phi(pk ) = (p1 − 1) \cdot (p2 − 1) \cdot ... \cdot (pk − 1) 
$$

Für unseren Spezialfall, also ein Produkt aus zwei Primzahlen gilt daher:
$$ \phi(p \cdot q) = \phi(p) \cdot \phi(q) = (p - 1) \cdot (q - 1) \text{ mit } p \in \mathbb{P} $$

Für unser Beispiel mit den Primzahlen $23$ und $17$ gilt daher:
$$ \phi(23 \cdot 17) = \phi(23) \cdot \phi(17) = (23 - 1) \cdot (17 - 1) = 352 $$

RSA (jetzt aber wirklich)
=========================

Generieren eines Schlüsselpaares (public- und private key)
----------------------------------------------------------

**1. Wähle zwei Primzahlen $p, q \in \mathbb{P}$**

~~~python
import random
p = random.choice(primes[-50:])
q = random.choice(primes[-50:])
print(f'p = {p}, q = {q}')
~~~

~~~
 p = 797, q = 883
~~~

**2. Berechne $n$ als Produkt der Zahlen $p$ und $q$.**

$n$ ist das *RSA-Modul*.

~~~python
     n = p * q
     print(f'n = {n}')
~~~

~~~
 n = 703751
~~~

**3. Berechne $\phi(n)$.**

~~~python
phi = (p - 1) * (q - 1)
print(f'phi = {phi}')
~~~

~~~
 phi = 702072
~~~

**4. Finde eine Zahl $e$, für die gilt:**

$$ 1 < e < \phi(n) \text{ mit } ggT(e, \phi(n)) = 1 $$

$e$ ist der öffentliche Exponent.

~~~python
e = 1
while e <= 1 or e > phi or euklid(e, phi)[0] != 1:
    e = random.choice(primes[-100:])
print(f'e = {e}')
~~~

~~~
 e = 631
~~~

**5. Die beiden Zahlen $e$ und $n$ sind der öffentliche Schlüssel (oder public Key).**

$(e, n)$ kann veröffentlicht werden.  
Alles andere $(p, q, \phi(n))$ muss geheim bleiben!

~~~python
public_key = (e, n)
print(f'public key = {public_key}')
~~~

~~~
 public key = (631, 703751)
~~~

**6. Bestimme $d$ damit $ggT(e, \phi(n)) = 1 = e \cdot d + \phi(n) \cdot k$ gilt.**

$k$ wird nicht benötigt.  
$d$ ist der geheime (oder private) Exponent.

~~~python
_ggT, d, _k = euklid(e, phi)
if d < 0:
    d += phi
print(f'd = {d}')
~~~

~~~
 d = 124615
~~~

**7. Die beiden Zahlen $d$ und $n$ sind der geheime Schlüssel (oder private Key).**

$(d, n)$ muss geheim bleiben.  
Alles außer $(e, n)$ und $(d, n)$ sollte aus Sicherheitsgründen gelöscht werden.

~~~python
private_key = (d, n)
print(f'private key = {private_key}')
~~~

~~~
 private key = (124615, 703751)
~~~
   
Eine Nachricht verschlüsseln
----------------------------

Um eine Nachricht zu verschlüsseln wird folgende Formel genutzt:
$$ G = K^e \bmod n $$
wobei $G$ der Geheimtext und $K$ der Klartext sind.

~~~python
# crypt ver- und entschlüsselt.
# k  ist ein schlüsselpaar der form (e, n) bzw. (d, n)
# m  ist die message (Nachricht)                            
crypt = lambda k, m: (m ** k[0]) % k[1]

K = 420
G = crypt(public_key, K)
print(f'aus    K = {K}\nwurde  G = {G}')
~~~

~~~
 aus    K = 420
 wurde  G = 545480
~~~

Eine Nachricht entschlüsseln
----------------------------

Um einen Geheimtext zu entschlüsseln wird die selbe Formel verwendet, wie zum Verschlüsseln.
Statt dem public key muss man nun den passenden private key verwenden.
$$ K = G^d \bmod n $$
wobei $K$ wieder der Klartext und $G$ wieder der Geheimtext (die verschlüsselte Nachricht) ist.

~~~python
K = crypt(private_key, G)
print(f'aus    G = {G}\nwurde  K = {K}')
~~~

~~~
 aus    G = 545480
 wurde  K = 420
~~~
