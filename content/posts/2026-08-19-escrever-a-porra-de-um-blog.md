---
title: Escrever a porra de um blog também
date: 2026-08-19
category: posts
tags: [blog, servidor, delírio]
preview: Montei um servidor. E pra conferir se ele continua de pé eu abro a porra do blog — e a porra do blog está ali, LINDUUU.
---

Montei um servidor. Debian, Docker, um túnel do Cloudflare, tudo bonitinho, tudo
funcionando. E aí vem a pergunta que todo mundo que monta servidor em casa faz
umas quarenta vezes por dia: será que ele continua de pé?

Tem jeito certo de conferir isso. Tem healthcheck no compose, tem `docker ps`,
tem uptime, tem log. Eu não uso nenhum. Eu abro a porra do blog.

E a porra do blog está ali. LINDUUU.

## O cron

De três em três dias a máquina puxa o repositório sozinha. Uma linha no
crontab, nada mais:

```cron
0 6 */3 * * git -C ~/KozatoBlog pull -q
```

O app relê os markdown a cada acesso, então não tem restart, não tem build, não
tem deploy. Publicar é o arquivo la e ele vai ta la. 

O efeito colateral é que a mesma olhada me responde duas coisas. Se a página
abre, o servidor está vivo. Se tem post novo, eu escrevi alguma coisa nos
últimos três dias. Quase sempre é só a primeira.

## O fórum

Antes disso eu tinha pensado em fórum. Era o que eu realmente queria — aquela
coisa de tópico que dura seis meses, gente respondendo por cima da resposta do
outro, assinatura com gif animado, moderador implicando com off-topic.

Mas fórum sem gente é cemitério. Fórum é das poucas coisas que não dá pra
fazer sozinho: dez posts meus num fórum meu não é comunidade, é diário com
paginação. Saudade não constrói fórum.

## Então

O [Dunossauro](https://dunossauro.com) falou que eu deveria criar a porra de um
blog. E ele me apresentou pela 142º vez o [Crie a Porra de Um Blog](https://crieaporradeum.blog/) dizendo exatamente isso
pra quem, como eu, prefere passar seis meses escolhendo gerador estático a
escrever um parágrafo.

E eu criei a porra disso aqui que... quanta porra, amigo.

Bom, é isso. Obrigado.
Em resumo do resumo, criei meu blog vou colocar aqui alguns textos, alguns coisas legais, alguns delirio ou apresentar meus projetos e conceitos.
