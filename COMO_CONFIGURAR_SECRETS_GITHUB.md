# 🔐 Como Configurar Secrets no GitHub

Guia passo a passo para configurar os secrets necessários no GitHub Actions.

## 📋 Secrets Necessários

Você precisa configurar 3 secrets:
1. `AWS_ACCESS_KEY_ID` - Credencial de acesso AWS
2. `AWS_SECRET_ACCESS_KEY` - Chave secreta AWS
3. `OPENAI_API_KEY` - Chave da API OpenAI

---

## 🔑 Passo 1: Obter OPENAI_API_KEY

### Se você já tem:
- Use a mesma chave que está no seu arquivo `.env` local

### Se não tem:
1. Acesse: https://platform.openai.com/api-keys
2. Clique em **"+ Create new secret key"**
3. Copie a chave (começa com `sk-`)

---

## ☁️ Passo 2: Criar Credenciais AWS

### 2.1 Acessar o Console AWS

1. Acesse: https://console.aws.amazon.com/
2. Faça login na sua conta AWS

### 2.2 Criar Usuário IAM para GitHub Actions

1. No console AWS, procure por **"IAM"** (Identity and Access Management)
2. No menu lateral, clique em **"Users"** (Usuários)
3. Clique no botão **"Create user"** (Criar usuário)

### 2.3 Configurar o Usuário

**Passo 1: Nome do Usuário**
- Nome: `IsCoolGPT-GitHubActions`
- Clique em **"Next"**

**Passo 2: Permissões**
- Selecione **"Attach policies directly"**
- Procure e selecione a política: **"IsCoolGPT-GitHubActionsPolicy"**
  - ⚠️ Se ainda não criou essa política, veja a seção abaixo
- Clique em **"Next"**

**Passo 3: Revisar e Criar**
- Revise as informações
- Clique em **"Create user"**

### 2.4 Criar Access Key

1. Clique no usuário recém-criado (`IsCoolGPT-GitHubActions`)
2. Vá para a aba **"Security credentials"** (Credenciais de segurança)
3. Role até a seção **"Access keys"**
4. Clique em **"Create access key"**
5. Selecione o caso de uso: **"Application running outside AWS"**
6. Clique em **"Next"**
7. (Opcional) Adicione uma descrição: "GitHub Actions CI/CD"
8. Clique em **"Create access key"**
9. **IMPORTANTE**: Copie imediatamente:
   - **Access key ID** (começa com `AKIA...`)
   - **Secret access key** (você só verá uma vez!)

---

## 📝 Passo 3: Criar Política IAM (Se ainda não criou)

Se você ainda não criou a política IAM, siga estes passos:

### 3.1 Criar Política

1. No IAM, clique em **"Policies"** (Políticas)
2. Clique em **"Create policy"**
3. Clique na aba **"JSON"**
4. Cole o seguinte conteúdo (ajuste o `ACCOUNT_ID`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:*:*:repository/iscoolgpt"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:UpdateService",
        "ecs:DescribeServices"
      ],
      "Resource": "arn:aws:ecs:*:*:service/*/iscoolgpt-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "codecommit:GitPush",
        "codecommit:GitPull",
        "codecommit:GetRepository"
      ],
      "Resource": "arn:aws:codecommit:*:*:iscoolgpt"
    }
  ]
}
```

5. Clique em **"Next"**
6. Nome da política: `IsCoolGPT-GitHubActionsPolicy`
7. Descrição: "Política para GitHub Actions fazer deploy"
8. Clique em **"Create policy"**

### 3.2 Anexar Política ao Usuário

1. Volte para **"Users"**
2. Clique no usuário `IsCoolGPT-GitHubActions`
3. Clique em **"Add permissions"**
4. Selecione **"Attach policies directly"**
5. Procure e selecione `IsCoolGPT-GitHubActionsPolicy`
6. Clique em **"Add permissions"**

---

## 🐙 Passo 4: Adicionar Secrets no GitHub

### 4.1 Acessar Configurações do Repositório

1. Acesse seu repositório no GitHub
2. Clique em **"Settings"** (Configurações) no topo do repositório
3. No menu lateral esquerdo, clique em **"Secrets and variables"**
4. Clique em **"Actions"**

### 4.2 Adicionar OPENAI_API_KEY

1. Clique no botão **"New repository secret"** (Novo secret do repositório)
2. **Name**: `OPENAI_API_KEY`
3. **Secret**: Cole sua chave da OpenAI (começa com `sk-`)
4. Clique em **"Add secret"**

### 4.3 Adicionar AWS_ACCESS_KEY_ID

1. Clique em **"New repository secret"** novamente
2. **Name**: `AWS_ACCESS_KEY_ID`
3. **Secret**: Cole o Access Key ID da AWS (começa com `AKIA...`)
4. Clique em **"Add secret"**

### 4.4 Adicionar AWS_SECRET_ACCESS_KEY

1. Clique em **"New repository secret"** novamente
2. **Name**: `AWS_SECRET_ACCESS_KEY`
3. **Secret**: Cole o Secret Access Key da AWS
4. Clique em **"Add secret"**

---

## ✅ Verificar se Está Configurado

Após adicionar os 3 secrets, você deve ver:

```
Secrets (3)
├── AWS_ACCESS_KEY_ID
├── AWS_SECRET_ACCESS_KEY
└── OPENAI_API_KEY
```

---

## 🧪 Testar a Configuração

### Opção 1: Fazer um Push

1. Faça uma pequena alteração no código
2. Commit e push:
```bash
git add .
git commit -m "test: verificar CI/CD"
git push origin develop
```

3. Vá para a aba **"Actions"** no GitHub
4. Você verá o workflow rodando

### Opção 2: Criar um Pull Request

1. Crie uma branch:
```bash
git checkout -b test-ci
```

2. Faça uma alteração qualquer
3. Commit e push:
```bash
git add .
git commit -m "test: verificar CI"
git push origin test-ci
```

4. Crie um Pull Request no GitHub
5. O workflow de CI será executado automaticamente

---

## 🔒 Segurança

### ✅ Boas Práticas

- ✅ Secrets nunca aparecem nos logs do GitHub Actions
- ✅ Secrets são mascarados automaticamente
- ✅ Apenas usuários com permissão podem ver/editar secrets
- ✅ Use o princípio do menor privilégio nas políticas IAM

### ⚠️ Cuidados

- ⚠️ **NUNCA** commite credenciais no código
- ⚠️ **NUNCA** compartilhe suas chaves
- ⚠️ Se uma chave for exposta, **revogue imediatamente**
- ⚠️ Use chaves diferentes para desenvolvimento e produção

---

## 🆘 Troubleshooting

### Erro: "Invalid credentials"
- Verifique se copiou as chaves corretamente
- Certifique-se de que não há espaços antes/depois
- Verifique se o usuário IAM tem as permissões corretas

### Erro: "Access denied"
- Verifique se a política IAM está anexada ao usuário
- Verifique se os recursos na política estão corretos (ARNs)

### Workflow não executa
- Verifique se os arquivos `.github/workflows/*.yml` estão no repositório
- Verifique se o branch está correto (develop, staging, main)
- Verifique se os secrets estão configurados corretamente

---

## 📚 Próximos Passos

Após configurar os secrets:

1. ✅ Teste o workflow de CI (testes, linting)
2. ✅ Configure a infraestrutura AWS (ECR, ECS)
3. ✅ Teste o deploy para staging
4. ✅ Configure monitoramento

---

**Pronto! Seus secrets estão configurados e seguros! 🔐**

