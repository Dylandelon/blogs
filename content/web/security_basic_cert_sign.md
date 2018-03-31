Title: 网络安全的基础 - 数字证书及签名
Date: 2018-03-31 23:52
Modified: 2018-03-31 23:52
Tags: web
Slug: security-basic-cert-sign
Authors: Joey Huang
Summary: 网络中怎么样确保数字内容是可信的？比如，怎么确保你连接的是招商银行的网站，而不是某李鬼的网站呢？本文将试着回答这个问题。
Status: draft

你哼着小曲，打开招商银行的网站，想查查看今年的奖金到账了没有。突然，一个想法惊出你一身冷汗：万一打开的是李鬼的招商银行网站，一输入密码登录，不是密码全被不法分子窃取了么？你瞄了一眼浏览器左上角地址栏上的标识，有一个绿色的大钩，说明这是一个可信的网站。你放心地输入了密码。

可是你有没有想过，为什么这个绿色的大钩能证明这是个可信的招商银行网站，而不是某李鬼银行网站呢？要回答这个问题，得从数字证书及数字签名的原理谈起。

生成密钥：

```shell
openssl genrsa -out rsa_private.key 2048
```

生成对应的公钥：

```shell
openssl rsa -in rsa_private.key -pubout -out rsa_public.key
```

生成密码保护的密钥：

```shell
openssl genrsa -aes256 -passout pass:yourpwd -out rsa_aes_private.key 2048
```

加密私钥转非加密：

```shell
openssl rsa -in rsa_aes_private.key -passin pass:111111 -out rsa_private.key
```

明文私钥转加密私钥：

```shell
openssl rsa -in rsa_private.key -aes256 -passout pass:111111 -out rsa_aes_private.key
```

使用 已有RSA 私钥生成自签名证书：

```shell
openssl req -new -x509 -days 365 -key rsa_private.key -out cert.crt -subj "/C=CN/ST=FJ/L=XM/O=sfox/OU=dev/CN=sfox.com/emailAddress=sfox@sfox.com"
```

使用己有的 RSA 私钥生成 CSR 签名请求：

```shell
openssl req -new -key rsa_private.key -out cert.csr -subj "/C=CN/ST=FJ/L=XM/O=sfox/OU=dev/CN=sfox.com/emailAddress=sfox@sfox.com
```

查看 CSR 的细节：

```shell
openssl req -noout -text -in cert.csr
```

使用 CA 证书及 CA 密钥对请求签名的证书进行签名，生成 X509 证书：

```shell
openssl x509 -req -days 3650 -in cert.csr -CA ca.crt -CAkey ca.key -passin pass:yourpwd -CAcreateserial -out cert_ca_signed.crt
```

ca.crt 是 CA 证书，ca.key 是 CA 证书的私钥，-passin 是私钥的密码，如果私钥没有密码保护，这个参数可以省略。最终输出的是 cert_ca_signed.crt 就是 CA 签名的证书。

生成待签名的数字内容：

```shell
echo "This is my real word -- Joey" > data.txt
```

对数字内容进行签名，签名的时候使用的是私钥：

```shell
openssl dgst -sha256 -sign rsa_private.key -out data.hash data.txt
```

对数字内容进行签名检查，检查签名时使用的是公钥：

```shell
openssl dgst -sha256  -verify rsa_public.key -signature data.hash data.txt
```

如果没有公钥，可以从证书里解出公钥：

```shell
openssl x509 -in cert_ca_signed.crt -pubkey -noout > rsa_public.key
```

