Title: 网络安全的基础 - 数字证书及签名
Date: 2018-03-31 23:52
Modified: 2018-03-31 23:52
Tags: web
Slug: security-basic-cert-sign
Authors: Joey Huang
Summary: 网络中怎么样确保数字内容是可信的？比如，怎么确保你连接的是招商银行的网站，而不是某李鬼的网站呢？本文将试着回答这个问题。

## 写在前面

你哼着小曲，打开招商银行的网站，想查查看今年的奖金到账了没有。突然，一个想法惊出你一身冷汗：万一打开的是李鬼的招商银行网站，一输入密码登录，不是密码全被不法分子窃取了么？浏览器怎么判断这是一个可信的网站，而不是某李鬼网站呢？要回答这个问题，得从数字证书及数字签名的原理谈起。实际上，本文要介绍的这些知识，也是当前火热的区域链技术的基础。

## 摘要算法

要谈清楚这些问题，需要先了解一下摘要算法。摘要算法根据输入计算出摘要。

![摘要算法](https://raw.githubusercontent.com/kamidox/blogs/master/images/digest.png)

它的特点是：

1. 定长输出：不管输入的数据是是长还是短，只要选定了特定的摘要算法，其输出的长度就是固定的。比如 SHA256 输出的摘要算法就是 32 字节。
2. 碰撞概率低：绝对不碰撞是不可能的，但好的摘要算法能做到非常低的碰撞概率。从应用的角度来看，基本上可以理解为一个输入对应一个输出，当输入改变了，输出也跟着改变。
3. 单向性：摘要算法是不可逆的。一个输入对应着一个输出，但从输出无法倒推出输入。

## 数据指纹

摘要算法的这个特点经常被用来计算数据的指纹，然后进行指纹验证。常用的摘要算法有 SHA1, SHA256, MD5 等等。SHA256 摘要算法的输出是 32 个字节，MD5 的摘要算法是 16 字节。比如，网站登录时，用户会网页上输入密码，服务器端要对输入的密码进行验证。此时网页前端不必把密码直接发送给服务器去验证，而是使用摘要算法计算密码的指纹，并把这个摘要信息发送给服务器进行验证（这样可以减少密码被人截获的风险），这样服务器只要拿相同的摘要算法也算一下密码的摘要，对比两个摘要是否相同即可知道用户输入的密码是否正确。

*备注：服务器的规范做法，不会保存密码的原文在数据库里的，一般通用的做法是生成一个随机的盐值，称为 salt，然后计算并保存密码加盐的摘要。*

另外一个常用的场景是，对文件的完整性进行验证。比如，你从网站上下载了一个文件，下载提供方还会提供这个文件的 MD5 摘要信息，你把这个文件下载下来后，可以计算一下这个文件的 MD5 摘要，然后和网站提供的 MD5 对比，如果一样，说明下载下来的文件是完整的；如果不一致，说明下载下来的文件是不完整的。

## 非对称加密算法

非对称加密算法和摘要算法，构成了数字签名和数字证书的基础。非对称加密算法的最大特点是：**加密时使用的密钥和解密时使用的密钥是不一样的**。即，非对称加密算法有两套密码，分别称为**私钥**和**公钥**，私钥私密保存，只有自己知道；公钥可以发给通信的对端。私钥加密的数据，只有对应的公钥能解密，公钥加密的信息，只有私钥能解密。用大白话，使用非对称加密算法来加密通信的数据后，我对外发的信息别人都能解读（因为公钥任何人都可以得到，是公开的），但别人给我发的信息，只有我能解读（因为只有我自己有私钥，能解密）。

![加密](https://raw.githubusercontent.com/kamidox/blogs/master/images/rsa_encrypt.png)

![解密](https://raw.githubusercontent.com/kamidox/blogs/master/images/rsa_decrypt.png)

*备注：与非对称加密算法对应的是对称加密算法。对称加密算法的密码只有一个，通信双方共享这个密码。常用的对称加密算法有 AES, DES 等。*

## 数字签名

常用的非对称加密算法有 RSA 和 ECC 等。非对称算法最经典的应用，是结合摘要算法对数据进行签名。现实生活中，签名的物理意义，是表示签下名字的主体认可被签名数据的有效性。比如，纸面签名是使用笔写上自己的名字，在签名认证时，通过确认笔迹来进行确认。那么，在数字世界中，怎么样进行数字签名呢？数字签名的步骤如下：

1. 选择合适的摘要算法（如 SHA256）计算出待签名数据的摘要
2. 使用**私钥**对摘要进行加密，输出的密文就是数据的**签名**

![签名](https://raw.githubusercontent.com/kamidox/blogs/master/images/digital_sign.png)

对签名进行检查的步骤如下：

1. 使用**公钥**对签名进行解密，解密出来的就是数据的摘要
2. 使用与签名时相同的摘要算法计算出数据的摘要
3. 对比步骤 1 和步骤 2 的摘要，如果相同，则说明签名有效，否则说明数据是无效的

![签名检查](https://raw.githubusercontent.com/kamidox/blogs/master/images/digital_sign_verify.png)

假设，有人偷偷篡改了数据，由于数字签名是没办法改变的，因为数字签名是经过私密保存的**私钥**加密过的，别人没有私钥，故无法对数字签名进行修改。在验证签名时，上述步骤 2 算出来的摘要（被篡改后的数据算出来的摘要）和步骤 1 算出来的摘要（用公钥直接解密的，原数据的摘要）必定不相同，这样就可以验证出来数据被人篡改了。

## 证书签名

有了数字签名的算法，我们就可以对实体颁发数字证书，然后让有公信力的机构对数字证书进行签名，这样就可以证明实体的真实身份。数字证书的主体内容包含三部分主要内容：

1. 证书基本信息：如证书的实体的名称，邮件地址，签发者，有效期等
2. 公钥：通信对端可以从数字证书里得到公钥，这样就可以对私钥加密过的数据进行解密
3. 数字签名：这个证书的数字签名。签名就是计算证书的摘要，然后用签发者的私钥进行加密后的数据

老牌的提供数字签名服务的机构是 VeriSign，交纳一定的费用，VeriSign 可以使用他们的 CA 证书给你的数字证书进行签名。这样主流的浏览器就会认可这个证书，并认为使用了这个证书的网站是安全的。问题是 VeriSign 怎么做到的呢？

实际上，VeriSign 以他们的信誉背书，生成了一个根证书，这个根证书是自签名的。即 VeriSign 在法律层面上要负责这个根证书的真实性和有效性。万一哪一天 VeriSign 的根证书的私钥泄漏了，被不法分子拿去，不法分子完全可以使用这个私钥，给一些恶意网站的证书进行签名。当用户打开这些恶意网站时，浏览器就不会提示用户。相反，浏览器会认为这是一个可信的网站。

有了根证书，VeriSign 就可以用根证书，按照不同的业务和行业签发一堆专用的 CA 证书出来，然后再用 CA 证书去给具体的实体的数字证书进行签名。浏览器验证实体的数字证书的合法性时，先检查这个证书的签名是否正确，然后检查给这个证书签名的 CA 证书的合法性。这样沿着**证书链**一步步往上验证，最终验证到了根证书。由于浏览器内置了 VeriSign 的根证书，故浏览器知道这个证书是合法的。浏览器就是这样判断一个网站的证书是否是可信的。

比如下图是招商银行的证书：

![证书链](https://raw.githubusercontent.com/kamidox/blogs/master/images/cert_chain.png)

从图中可以看到，招商银行的证书是由 Symantec Class 3 EV SSL CA - G3 这个 CA 证书签名的，而这个 CA 证书又是由 VeriSign Class 3 Public Primary Certification Authority - G5 这个证书签名的。这样也就不难理解，为什么 VeriSign 在给你的网站的数字证书进行签名时需要收取费用：实际上这是一个名誉背书的费用。技术角度来看，运行一条指令就可以对你的数字证书进行签名，没有任何的成本，但 VeriSign 必须在法律层面保证，他们签名的对象是个可信的实体。

实际上，你完全可以生成一个自签名的证书，即用你自己生成的证书的私钥给你自己的证书签名。这是完全合法的，但浏览器往往不认可这种自签名证书，并且提示用户说，这个网站的证书是不可信的。

## 实践出真知

如果你对技术细节不感兴趣，这篇文章阅读到此就可以结束了。本节演示如何使用 openssl 工具包，对数据进行数字签名及验证，以及对证书进行签名。

### 信息摘要

我们先把要计算摘要的数据保存到 `data.txt` 文件里：

```shell
$ echo "This is real words from Joey." > data.txt
```

然后以这个文件作为输入计算 SHA256 摘要信息：

```shell
$ openssl dgst -sha256 -hex data.txt
```

其输出为：

```shell
SHA256(data.txt)= f1b1b3f5f35944c8e2169031efac2a37147dac631b8dbd7cfa5d265e0e804e8d
```

当然，我们也可以换成 MD5 算法并计算其摘要：

```shell
$ openssl dgst -md5 -hex data.txt
MD5(data.txt)= ed764086c5770a9d5ff0e60036aa4226
```

从输出不难看出，SHA256 的摘要输出是 32 个字节（f1 是第一个字节，b1 是第二个字节，依此类推），MD5 的摘要输出是 16 字节。

### 非对称加密算法

我们先生成一个 2048 bit 的 RSA 算法私钥：

```shell
$ openssl genrsa -out rsa_private.key 2048
```

`rsa_private.key` 就是生成的私钥。这是个文本文件，你可以用任何文本编辑器打开它，内容如下：

```text
-----BEGIN RSA PRIVATE KEY-----
BASE64(PRIVATE KEY)
-----END RSA PRIVATE KEY-----
```

私钥数据是经过 BASE64 编码的数据，故显示成 ASCII 字符。私钥必须私密保存，一旦泄漏，整个安全体系就崩塌了。由于私钥是如此的重要，openssl 提供了一个方法来加密保存私钥文件。下面的命令用来生成密码保护的密钥：

```shell
$ openssl genrsa -aes256 -passout pass:yourpwd -out rsa_aes_private.key 2048
```

这个命令生成的私钥 `rsa_aes_private.key` 是使用 AES 256 算法加密保存的，密码就是字符串 `yourpwd` 。下次使用这个私钥时，就必须提供这个密码才能使用。我们还可以把加密保存的私钥转为不加密的，其命令为：

```shell
$ openssl rsa -in rsa_aes_private.key -passin pass:yourpwd -out rsa_private.key
```

当然，明文的私钥也可以加密保存起来：

```shell
$ openssl rsa -in rsa_private.key -aes256 -passout pass:newpwd -out rsa_aes_private.key
```

有了私钥，我们就可以生成与之配套使用的公钥：

```shell
$ openssl rsa -in rsa_private.key -pubout -out rsa_public.key
```

`rsa_public.key` 就是对应的公钥。公钥文件也是一个纯文本文件，其内容示意如下：

```text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA69EVk9GKyEQDRfV8OJUf
49eaJ67bTP/zAPm5huf9z7EhAaltjyfHNaCQMYVTAKUAS9c7XhKxA8NkHil/HNBE
4UONY054voisKWYqxtHaoFkcfY5QE+vj9JVJajwYAKZjA362zo2y8qbpJ6INCMeB
19oOuGFBTkn4z0RR71kFriyQ2pOjbHru5pH9bC9t4GjvkNMNWeFdSdR3uO3zIYB6
cl176kaYZ8Bwr+PeGl+jzMpd7lDSEVLLaAt1jZiNLQ1dYTN4GGuURy/6b3d4+TZ1
VxNlLc0+8l+vyzpXRZWxZcEBjA4voeWmxqBKUsA6jKTDS/V6IFOTakoOGLk5w3f1
EQIDAQAB
-----END PUBLIC KEY-----
```

### 证书及签名

#### 生成自签名证书

使用已有 RSA 算法的私钥生成自签名证书：

```shell
$ openssl req -new -x509 -days 365 -key rsa_private.key -out cert.crt -subj "/C=CN/ST=FJ/L=XM/O=sfox/OU=dev/CN=sfox.com/emailAddress=sfox@sfox.com"
```

-days 参数指明这个证书的有效期；-key 参数指定使用的 RSA 私钥文件；-out 参数指定输出的自签名证书文件，一般以 crt 作为后缀名；-subj 参数用来指定证书的名称，如果不带这个参数，则需要逐个输入证书的名称参数，包含国家，省份，城市，组织名称，部门名称，通用名称等等。

可以使用下面命令来查看自签名证书的信息：

```shell
$ openssl x509 -in cert.crt -noout -text
```

其输出示意如下：

```text
Certificate:
    Data:
        Version: 1 (0x0)
        Serial Number: 11926462855904995145 (0xa5834ec7411ba749)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CN, ST=FJ, L=XIAMEN, O=SFOX, OU=SW, CN=sfox/emailAddress=sfox@qq.com
        Validity
            Not Before: Mar 31 13:35:11 2018 GMT
            Not After : Mar 31 13:35:11 2019 GMT
        Subject: C=CN, ST=FJ, L=XIAMEN, O=SFOX, OU=SW, CN=sfox/emailAddress=sfox@qq.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:eb:d1:15:93:d1:8a:c8:44:03:45:f5:7c:38:95:
                    1f:e3:d7:9a:27:ae:db:4c:ff:f3:00:f9:b9:86:e7:
                    fd:cf:b1:21:01:a9:6d:8f:27:c7:35:a0:90:31:85:
                    53:00:a5:00:4b:d7:3b:5e:12:b1:03:c3:64:1e:29:
                    7f:1c:d0:44:e1:43:8d:63:4e:78:be:88:ac:29:66:
                    2a:c6:d1:da:a0:59:1c:7d:8e:50:13:eb:e3:f4:95:
                    49:6a:3c:18:00:a6:63:03:7e:b6:ce:8d:b2:f2:a6:
                    e9:27:a2:0d:08:c7:81:d7:da:0e:b8:61:41:4e:49:
                    f8:cf:44:51:ef:59:05:ae:2c:90:da:93:a3:6c:7a:
                    ee:e6:91:fd:6c:2f:6d:e0:68:ef:90:d3:0d:59:e1:
                    5d:49:d4:77:b8:ed:f3:21:80:7a:72:5d:7b:ea:46:
                    98:67:c0:70:af:e3:de:1a:5f:a3:cc:ca:5d:ee:50:
                    d2:11:52:cb:68:0b:75:8d:98:8d:2d:0d:5d:61:33:
                    78:18:6b:94:47:2f:fa:6f:77:78:f9:36:75:57:13:
                    65:2d:cd:3e:f2:5f:af:cb:3a:57:45:95:b1:65:c1:
                    01:8c:0e:2f:a1:e5:a6:c6:a0:4a:52:c0:3a:8c:a4:
                    c3:4b:f5:7a:20:53:93:6a:4a:0e:18:b9:39:c3:77:
                    f5:11
                Exponent: 65537 (0x10001)
    Signature Algorithm: sha256WithRSAEncryption
         b3:41:be:6f:54:3c:d7:fc:53:c6:21:f5:ea:fa:2d:c7:70:ed:
         29:57:c4:0b:74:43:74:24:1b:05:df:2e:9f:ef:76:32:8a:8e:
         4a:85:31:18:a2:50:95:1a:6e:07:cf:e9:82:04:55:ee:1b:26:
         0a:e7:bf:47:ef:d5:69:d1:ef:fb:db:50:52:84:2d:85:e9:2c:
         15:5c:de:2d:9c:74:fe:90:b9:02:29:1b:dc:fb:b8:ef:08:b2:
         04:0c:27:66:c8:f1:31:a6:f3:52:73:4b:16:41:0d:f1:a9:d5:
         f2:1b:60:3a:44:a0:be:35:ef:a6:e4:10:bf:90:4e:98:3f:56:
         3e:3d:ef:99:b2:38:97:2b:5a:f9:46:61:4a:e1:77:9e:76:0a:
         3a:d6:2f:f2:16:31:8c:cf:e5:e4:e5:42:14:07:8c:fa:a6:48:
         19:76:cd:6d:63:8e:62:a2:65:83:9f:9d:c4:d6:32:97:6a:54:
         e6:27:49:30:aa:08:72:0c:2f:e0:9a:a1:ae:2a:75:34:ad:31:
         0f:26:71:7e:6f:75:d4:cc:d3:58:13:2c:18:da:2d:ef:a1:e6:
         7a:9a:d1:d4:1d:48:b4:ac:06:84:8b:07:1b:15:9c:f8:e5:fe:
         ac:58:c4:50:74:a9:8e:c2:f9:24:01:a2:d1:83:92:41:96:fa:
         bb:42:73:7a
```

#### 生成签名请求文件

当需要申请使用 CA 证书对证书进行签名时，需要生成签名请求文件。使用己有的 RSA 私钥生成签名请求文件的命令为：

```shell
$ openssl req -new -key rsa_private.key -out cert.csr -subj "/C=CN/ST=FJ/L=XM/O=sfox/OU=dev/CN=sfox.com/emailAddress=sfox@sfox.com
```

其中 -key 指定证书的私钥信息，openssl 命令会使用私钥来算出公钥，并把公钥包含在证书文件里；-out 指明要生成的证书签名请求文件的文件名，一般以 csr 作为后缀；-subj 表示待签名的证书的名称信息。生成的证书请求文件可以使用如下命令来查看详情：

```shell
$ openssl req -noout -text -in cert.csr
Certificate Request:
    Data:
        Version: 0 (0x0)
        Subject: C=CN, ST=FJ, L=XM, O=SFOX, OU=SW, CN=sfox.com/emailAddress=sfox@qq.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:eb:d1:15:93:d1:8a:c8:44:03:45:f5:7c:38:95:
                    1f:e3:d7:9a:27:ae:db:4c:ff:f3:00:f9:b9:86:e7:
                    fd:cf:b1:21:01:a9:6d:8f:27:c7:35:a0:90:31:85:
                    53:00:a5:00:4b:d7:3b:5e:12:b1:03:c3:64:1e:29:
                    7f:1c:d0:44:e1:43:8d:63:4e:78:be:88:ac:29:66:
                    2a:c6:d1:da:a0:59:1c:7d:8e:50:13:eb:e3:f4:95:
                    49:6a:3c:18:00:a6:63:03:7e:b6:ce:8d:b2:f2:a6:
                    e9:27:a2:0d:08:c7:81:d7:da:0e:b8:61:41:4e:49:
                    f8:cf:44:51:ef:59:05:ae:2c:90:da:93:a3:6c:7a:
                    ee:e6:91:fd:6c:2f:6d:e0:68:ef:90:d3:0d:59:e1:
                    5d:49:d4:77:b8:ed:f3:21:80:7a:72:5d:7b:ea:46:
                    98:67:c0:70:af:e3:de:1a:5f:a3:cc:ca:5d:ee:50:
                    d2:11:52:cb:68:0b:75:8d:98:8d:2d:0d:5d:61:33:
                    78:18:6b:94:47:2f:fa:6f:77:78:f9:36:75:57:13:
                    65:2d:cd:3e:f2:5f:af:cb:3a:57:45:95:b1:65:c1:
                    01:8c:0e:2f:a1:e5:a6:c6:a0:4a:52:c0:3a:8c:a4:
                    c3:4b:f5:7a:20:53:93:6a:4a:0e:18:b9:39:c3:77:
                    f5:11
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha256WithRSAEncryption
         13:aa:fc:0f:82:a4:b1:cf:3a:f3:3f:ff:53:b8:50:e8:41:cc:
         6b:a3:1c:5b:e2:4d:b0:47:f3:02:a8:ae:34:22:94:fc:8d:6b:
         11:41:82:33:9f:b1:df:da:fd:90:18:55:5d:aa:9e:61:82:26:
         e0:b5:9e:86:0d:18:cb:8d:e4:f5:d3:2c:32:8d:21:9d:f8:c2:
         3d:c8:22:e2:9c:10:69:bc:25:de:a4:14:05:c3:2c:c7:7b:d4:
         ee:30:53:9c:71:2f:0e:f5:04:83:54:d8:74:28:e9:ef:4a:72:
         b5:88:a5:73:d5:78:8e:27:88:be:52:16:fd:a9:cc:13:38:aa:
         1c:94:a4:20:a5:23:4d:bd:7d:29:d2:db:da:ec:86:2c:99:36:
         fb:c0:b2:0f:ec:da:ef:51:d5:f7:37:d0:11:59:d0:66:c4:e9:
         d1:ed:a1:2b:d4:b3:46:6b:fe:6f:17:3b:77:0c:be:f8:20:5b:
         ca:66:2d:64:17:20:5d:19:73:4d:be:5e:e3:fc:25:1a:cb:03:
         87:4d:55:7a:56:9d:ed:d7:7d:5a:55:e2:85:1b:2f:d2:fe:74:
         43:6f:84:5c:2b:de:c9:0c:05:76:08:65:de:6a:21:d6:26:0f:
         23:5a:12:4e:13:0e:8f:fd:ef:7c:e6:b4:6b:07:80:0f:2b:b8:
         7f:66:c7:16
```

细心的读者可以发现，证书签名请求文件和自签名的证书文件相比，少了 Issuer（颁发者），Serial Number，Validity（有效期）等信息。

#### 使用 CA 证书对 CSR 文件进行签名

要使用 CA 证书对签名请求文件进行签名，你必须有 CA 证书文件以及 CA 证书的私钥文件。有了这两个文件，可以使用下面的命令进行签名：

```shell
$ openssl x509 -req -days 3650 -in cert.csr -CA ca.crt -CAkey ca.key -passin pass:yourpwd -CAcreateserial -out cert_ca_signed.crt
```

-days 表示证书的有效期，此处指定 3650 表示 10 年有效期；-in 表示输入文件，此处是指证书请求签名文件的文件名；-CA 指定 CA 证书的文件名；-CAkey 指定 CA 证书的私钥文件；-passin 指定 CA 证书的私钥文件的加密密码，如果以明文保存的私钥文件，则此参数可省略。-CAcreateserial 参数指定给签名后的证书创建序列号；-out 参数指明输出的签名后的数字证书文件的文件名。

当然，这里你完全可以使用自签名的证书文件及其对应的私钥文件给其他的证书请求文件进行签名。

### 数字签名及验证

本小节将演示对一段文本内容进行签名，然后验证签名的正确性。

我们先生成待签名的数字内容：

```shell
$ echo "This is real words from Joey." > data.txt
```

接着，对数字内容进行签名，签名的时候使用的是**私钥**：

```shell
$ openssl dgst -sha256 -sign rsa_private.key -out data.sign data.txt
```

这个命令对 `data.txt` 文件的内容计算 SHA256 摘要；然后使用对输出的 32 字节的摘要信息，使用 `rsa_private.key` 指定的私钥进行加密，并把密文输出到 `data.sign` 文件里。`data.sign` 是个二进制文件，文件里保存的内容就是 `data.txt` 文件的数字签名。

接着，我们对数字内容进行签名检查，检查签名时使用的是公钥：

```shell
$ openssl dgst -sha256  -verify rsa_public.key -signature data.sign data.txt
```

不出意外的话，输出的内容为：

```text
Verified OK
```

表示数字签名验证成功，`data.txt` 文件的内容没有被篡改。现在，我们把 `data.txt` 文件修改一下，看看签名验证能否成功：

```shell
$ echo "This is fake words from Joey." > data.txt
$ openssl dgst -sha256  -verify rsa_public.key -signature data.sign data.txt
Verification Failure
```

此时输出的是 `Verification Failure` 表示数字签名验证失败。

当然，如果我们手头没有现成的公钥业验证签名，只要有这个网站的证书，则可以可以从证书里获取到公钥：

```shell
openssl x509 -in cert_ca_signed.crt -pubkey -noout > rsa_public.key
```

（完）
