(() => {
  const apiBaseInput = document.getElementById('apiBaseUrl');
  const subjectSelect = document.getElementById('subject');
  const form = document.getElementById('chatForm');
  const chatOutput = document.getElementById('chatOutput');
  const messageInput = document.getElementById('message');
  const contextInput = document.getElementById('context');
  const clearButton = document.getElementById('clearChat');
  const toast = document.getElementById('toast');

  let conversation = [];
  let isLoading = false;

  const fallbackSubjects = [
    'Matemática',
    'Física',
    'Química',
    'Biologia',
    'História',
    'Geografia',
    'Português',
    'Inglês',
    'Programação',
    'Ciência da Computação'
  ];

  function getApiBase() {
    return apiBaseInput.value.trim().replace(/\/$/, '');
  }

  async function loadSubjects(showFeedback = false) {
    const baseUrl = getApiBase();
    const endpoint = `${baseUrl}/api/v1/subjects`;

    subjectSelect.innerHTML = '<option value="">Carregando disciplinas...</option>';

    try {
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`Erro ${response.status}`);
      }
      const data = await response.json();
      const subjects = data.subjects ?? fallbackSubjects;
      renderSubjects(subjects);
      if (showFeedback) {
        showToast('Disciplinas atualizadas a partir da API.');
      }
    } catch (error) {
      renderSubjects(fallbackSubjects);
      showToast('Usando lista padrão de disciplinas (falha ao consultar a API).', true);
      console.error('Erro ao carregar disciplinas:', error);
    }
  }

  function renderSubjects(subjects) {
    subjectSelect.innerHTML = '<option value="">Selecione uma disciplina</option>';
    subjects.forEach((subject) => {
      const option = document.createElement('option');
      option.value = subject;
      option.textContent = subject;
      subjectSelect.appendChild(option);
    });
  }

  function renderConversation() {
    chatOutput.innerHTML = '';

    if (!conversation.length) {
      const placeholder = document.createElement('p');
      placeholder.className = 'placeholder';
      placeholder.textContent = 'Envie uma pergunta para ver a resposta do IsCoolGPT.';
      chatOutput.appendChild(placeholder);
      return;
    }

    conversation.forEach((message) => {
      const wrapper = document.createElement('div');
      wrapper.className = `message ${message.role}`;

      const header = document.createElement('div');
      header.className = 'message-header';
      header.innerHTML = `
        <span>${message.role === 'user' ? 'Você' : 'IsCoolGPT'}</span>
        <time>${new Intl.DateTimeFormat('pt-BR', {
          hour: '2-digit',
          minute: '2-digit'
        }).format(message.timestamp)}</time>
      `;

      const body = document.createElement('div');
      body.className = 'message-body';
      body.textContent = message.content;

      wrapper.appendChild(header);
      wrapper.appendChild(body);
      chatOutput.appendChild(wrapper);
    });

    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  function setLoading(state) {
    isLoading = state;
    form.querySelector('button[type="submit"]').disabled = state;
    form.querySelector('button[type="submit"]').textContent = state
      ? 'Enviando...'
      : 'Enviar pergunta';
  }

  function showToast(message, isError = false) {
    toast.textContent = message;
    toast.style.background = isError ? 'rgba(239, 68, 68, 0.95)' : 'rgba(37, 99, 235, 0.95)';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3200);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (isLoading) return;

    const message = messageInput.value.trim();
    const subject = subjectSelect.value.trim();
    const context = contextInput.value.trim();

    if (!message) {
      showToast('Digite uma pergunta antes de enviar.', true);
      return;
    }

    const baseUrl = getApiBase();
    if (!baseUrl) {
      showToast('Informe a URL da API.', true);
      return;
    }

    conversation.push({
      role: 'user',
      content: message,
      timestamp: new Date()
    });
    renderConversation();

    const payload = { message };
    if (subject) payload.subject = subject;
    if (context) payload.context = context;

    setLoading(true);

    try {
      const response = await fetch(`${baseUrl}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.detail || `Erro ${response.status}`);
      }

      const data = await response.json();
      conversation.push({
        role: 'assistant',
        content: data.response ?? 'Sem resposta fornecida pela API.',
        timestamp: new Date()
      });
      renderConversation();
      showToast('Resposta recebida!');
    } catch (error) {
      conversation.push({
        role: 'assistant',
        content: `Não foi possível obter resposta da API. Detalhes: ${error.message}`,
        timestamp: new Date()
      });
      renderConversation();
      showToast('Falha ao consultar a API. Verifique a URL e tente novamente.', true);
      console.error('Erro ao enviar mensagem:', error);
    } finally {
      setLoading(false);
      form.reset();
      subjectSelect.selectedIndex = 0;
      messageInput.focus();
    }
  });

  clearButton.addEventListener('click', () => {
    conversation = [];
    renderConversation();
    showToast('Histórico limpo.');
  });

  apiBaseInput.addEventListener('change', () => {
    loadSubjects(true);
  });

  loadSubjects();
})();
