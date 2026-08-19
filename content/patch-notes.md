# Patch Notes — Treino-UP

**Última atualização:** 17 de agosto de 2026
{: .updated }

Histórico de atualizações do Treino-UP (1.0.0 → 1.0.4), da versão mais recente
para a mais antiga. O detalhe técnico de cada release vive em `docs/patch-*.md`
e em `CHANGELOG.md`.
{: .intro }

## v1.0.4 — (atual)

**Renomeado para Treino-UP.** O nome do app deixa de ser "Academia-Treino-UP" e
passa a ser simplesmente **Treino-UP** (launcher, Capacitor e artefatos do APK).

### Check-in mais completo (`CheckinPage`) {: .tag-new }
- **Vontade de treinar**: nova escala 1–10, além do humor.
- **Dor por região**: o aluno marca as regiões do corpo (ombro, lombar, joelho,
  quadril, tornozelo) em vez de só descrever a dor em texto.
- **Prontidão para treinar em tempo real**: um card com score /100, cor por
  intensidade (verde/amarelo/rosa), barra de progresso e a recomendação que o
  personal vai ler — atualiza ao vivo enquanto o aluno preenche o check-in,
  antes de enviar.
- O detalhe do check-in no painel do treinador mostra os novos campos: card de
  "Vontade" e as regiões de dor marcadas como chips (antes ele tentava adivinhar
  a região procurando a palavra no texto).

### Mapa muscular {: .tag-new }
- Novo grupo muscular **Canela** (tibial anterior, fibular, extensores) desenhado
  no atlas anatômico — o mapa e o destaque por intensidade agora cobrem 18
  grupos.

### Catálogo de exercícios mais rápido e offline {: .tag-up }
- **Cache local de imagens**: as fotos do catálogo (antes baixadas do CDN a cada
  abertura) agora são guardadas no aparelho e servidas do disco — abre mais
  rápido e funciona offline. O download acontece sob demanda, só para as imagens
  que ficam perto da tela.
- **Janelamento do catálogo**: os 873 exercícios não são montados de uma vez —
  renderiza um lote e carrega o resto conforme a rolagem. Fim do engasgo na
  primeira abertura.
- CDN de imagens migrado de `raw.githubusercontent` para `cdn.jsdelivr`
  (mais rápido e confiável).

### Botão voltar (Android) mais confiável {: .tag-fix }
- O override do back agora tem **escopo por rota**: o handler de uma página
  anterior não "engole" mais o back da tela seguinte (bug que fazia a tela não
  sair em alguns fluxos, como o catálogo embutido em `/treinos`).
- Novo botão **simular hardware back** só em modo de desenvolvimento, para testar
  o mesmo caminho que roda no aparelho.

### Outros
- Seletor de grupos musculares do Progresso virou um **bottom sheet** em grade de
  2 colunas com destaque do grupo ativo.
- Corrida ao salvar: os últimos pontos ainda na fila do GPS são aplicados antes
  de encerrar — não perde mais os metros finais.
- Documentação reestruturada em `docs/01` a `docs/10` (arquitetura, backend,
  banco, frontend, portal, infra, regras, segurança, testes, Play Console).

## v1.0.3

### Sessão de treino ativa reformulada (`SessaoAtivaPage`) {: .tag-up }
- **Cabeçalho flutuante** (tempo/progresso): só em duas posições — encaixado no
  topo ou fixo como pill no rodapé — nunca mais flutuando no meio cobrindo as
  séries. Arraste para alternar, com snap suave.
- **Descanso integrado ao cabeçalho**, aparecendo só durante o intervalo.
- **Excluir série deslizando**: deslize revela o botão, deslize até o fim já
  remove, com renumeração automática, progresso atualizado na hora e toast
  "DESFAZER". Última série do exercício pede confirmação.
- **Carga do último treino já preenchida**: os campos KG e REPS entram com o que
  foi levantado na última vez (editável). Antes gravava o alvo da ficha quando o
  aluno não digitava.
- **Histórico "ANTERIOR" coerente**: as séries mostradas vêm todas da mesma
  sessão (a última em que o exercício foi feito), não mais da última ocorrência
  de cada série.
- Nova série adicionada herda a carga da última.

### Progresso {: .tag-fix }
- Corrigido o `padding` que escondia o último gráfico/sessão atrás da barra de
  abas fixa.

### Métricas mais honestas {: .tag-up }
- **Aquecimento fora dos cálculos**: volume, frequência, mapa muscular e
  progressão ignoram séries de aquecimento e incompletas — o warm-up não infla
  mais os números.
- **Técnica de cada série** (WU/DS/ISO) agora chega ao servidor e aparece no
  detalhe da sessão do painel do treinador.

### Dados Locais (`DadosLocaisPage`) {: .tag-up }
- Textos humanizados ("Salvar/Restaurar cópia de segurança"), exportação pelo
  **menu nativo do sistema** (Arquivos, Google Drive, WhatsApp…), arquivo com
  data (`backup_meu_treino_AAAA-MM-DD.json`), importação filtrada por `.json`,
  confirmação mostrando a data do backup, botão "Apagar todos os dados" em
  vermelho de alerta e nota de privacidade corrigida (o histórico já sincroniza
  com o servidor; a cópia local é um extra).

### Biblioteca e Editor de Plano (treinador) {: .tag-new }
- Busca e filtros por categoria, visualizar bloco em modo leitura, duplicar,
  salvar protegido, reordenar exercícios, **catálogo com seleção múltipla** e
  prévia do movimento.
- Biblioteca **repaginada em cards** com cor por tipo (Push/Pull/Legs…), menu ⋯
  no próprio card, toggle **Biblioteca / Catálogo** e mini-stats no topo.
- Catálogo virou componente único, compartilhado pela biblioteca e pelo editor.

### Painel do treinador {: .tag-up }
- Menu inferior com indicador pontual da aba ativa (accent turquesa).
- **Perfil repaginado** seguindo o padrão do aluno: cabeçalho com badge
  "TREINADOR", **avatar editável com corte de imagem** (antes não existia para o
  treinador), ações em blocos e Sair com confirmação.

### Corrida e rastreamento GPS {: .tag-up }
- **Grava com a tela apagada**: passou para o serviço em segundo plano, com
  notificação persistente.
- Permissões pedidas antes de começar (notificação + isenção de economia de
  bateria, só uma vez).
- **Filtro de ruído do GPS**: descarta leituras imprecisas e saltos impossíveis
  (limite maior no ciclismo) — fim dos "teleportes" que inflavam distância e
  pace.
- **Rota incompleta não some mais**: é salva e marcada, com aviso de sinal fraco
  na tela de detalhe.
- **Travamento corrigido**: gravação sai no máximo a cada 10s e as contas só
  refazem quando chega ponto novo; traçado com no máximo 300 vértices.
- **FC e calorias do relógio** buscadas do Health Connect ao encerrar.
- **Tempo é o do cronômetro** (antes era deduzido dos pontos do GPS e encolhia
  com sinal ruim).
- **Sinal fraco não zera a corrida**: após 30s sem leitura boa, aceita até 100m
  de incerteza enquanto o sinal não melhora.
- Um **motor de GPS único** para corrida e auto-rastreamento (sem competir).

### Servidor {: .tag-fix }
- Corrigido o **resgate de código de acesso** (erro 500 impedia o aluno de
  definir a senha e entrar).
- `POST /routes` aceita `durationSeconds` (tempo do cronômetro) e FC agregada da
  atividade (`avgHeartRateBpm`, `maxHeartRateBpm`) — Health Connect devolve só a
  média/máxima, não há como distribuir pelos pontos.

## v1.0.2

- **Catálogo de exercícios**: card não vaza mais por cima da barra de status
  durante o scroll (header de busca fixo fora da área de rolagem).
- **Busca por prefixo**: digitar "supi" já encontra "Supino" — vale para o
  catálogo e para o seletor do gerador de treino.
- **Perfil**: novo campo **sexo** (refina IMC e percentual de gordura), **avatar
  com corte de imagem**, e barra de status do Android alinhada ao tema.

## v1.0.1

- **Portal web do treinador** (`app.kozato.app.br`): login, roster de alunos com
  busca, seleção múltipla e desatribuição em massa, perfil do aluno, check-ins
  pendentes, atribuição de treino em massa, biblioteca de blocos, calendário de
  metas e criação de eventos de corrida em grupo.
- **Resiliência offline**: login não desloga por falha de rede (usa o último
  usuário válido em cache) e a sessão de treino sincroniza sozinha quando a
  conexão volta.
- **Backend em servidor dedicado**: migração de SQLite para **PostgreSQL**,
  Docker Compose único (dev = produção) atrás de Cloudflare Tunnel, backup
  diário para o Google Drive.
- **Corrida**: hub com evolução semanal, zonas de FC, planejamento de prova com
  tapering, e **importação de GPX**.
- Marca NORTE, "Coach" virou "Personal", e app renomeado para
  **Academia-Treino-UP**.
- Página de **privacidade** pública e manifest Android com permissões de saúde
  enxugadas (12 reais, justificadas no Play Console).

## v1.0.0 — Lançamento

Primeira versão publicada:

- App Android com os dois papéis: **treinador** (gerencia alunos, prescreve
  planos, acompanha sessões) e **aluno** (registra treinos, recebe feedback).
- Catálogo com **873 exercícios em PT-BR**, gerador de treino e rotinas.
- **Sessão de treino ao vivo** com cronômetro, séries/cargas e feedback por
  exercício.
- **Health Connect (leitura)**: passos, FC, calorias, peso e gordura.
- **Corrida ao ar livre** com GPS, mapa e histórico.
- Chat treinador↔aluno, check-ins, metas, conquistas, mapa muscular e 5 temas.
- Isolamento entre contas verificado por testes de segurança.

---

*Próxima versão em `docs/patch-*.md`. Página pública das notas: `https://kozato.app.br/patch-notes`.*
