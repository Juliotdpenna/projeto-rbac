
const API_URL = 'http://127.0.0.1:8000'

// O token permanece somente na memória da aplicação.
let accessToken = null

export function definirAccessToken(token) {
  accessToken = token
}

export function limparAccessToken() {
  accessToken = null
}

export async function fazerRequisicao(endpoint, opcoes = {}) {
  const headers = {
    ...opcoes.headers,
  }

  if (opcoes.body) {
    headers['Content-Type'] = 'application/json'
  }

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`
  }

  const resposta = await fetch(`${API_URL}${endpoint}`, {
    ...opcoes,
    headers,
  })

  const texto = await resposta.text()
  let dados = null

  if (texto) {
    try {
      dados = JSON.parse(texto)
    } catch {
      throw new Error('A API retornou uma resposta inválida.')
    }
  }

  if (!resposta.ok) {
  const detalhe = dados?.detail

  let mensagem = 'Ocorreu um erro na comunicação com a API.'

  if (typeof detalhe === 'string') {
    mensagem = detalhe
  } else if (Array.isArray(detalhe)) {
    mensagem = detalhe
      .map((item) => item.msg || 'Dados inválidos.')
      .join(' ')
  }

  throw new Error(mensagem)
}

  return dados
}
