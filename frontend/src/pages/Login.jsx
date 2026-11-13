import { useState } from 'react'
import {
  fazerRequisicao,
  definirAccessToken,
  limparAccessToken,
} from '../services/api'
import './Login.css'

function Login({ onLogin }) {
  const [mostrarSenha, setMostrarSenha] = useState(false)
  const [matricula, setMatricula] = useState('')
  const [senha, setSenha] = useState('')
  const [erros, setErros] = useState({})
  const [carregando, setCarregando] = useState(false)
  const [mensagem, setMensagem] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    if (carregando) {
      return
    }

    const novosErros = {}

    if (!matricula.trim()) {
      novosErros.matricula = 'Informe sua matrícula.'
    }

    if (!senha) {
      novosErros.senha = 'Informe sua senha.'
    }

    setErros(novosErros)
    setMensagem('')

    if (Object.keys(novosErros).length > 0) {
      return
    }

    setCarregando(true)
    limparAccessToken()

    try {
      const resultadoLogin = await fazerRequisicao('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          matricula: matricula.trim(),
          senha,
        }),
      })

      if (!resultadoLogin?.access_token) {
        throw new Error('A API não retornou um token válido.')
      }

      definirAccessToken(resultadoLogin.access_token)

      const dadosUsuario = await fazerRequisicao('/auth/me')

      setSenha('')
      onLogin(dadosUsuario)
    } catch (erro) {
      limparAccessToken()

      setMensagem(
        erro.message === 'Failed to fetch'
          ? 'Não foi possível conectar à API. Verifique se o backend está em execução.'
          : erro.message
      )
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="login-container">
      <section className="login-card">
        <div className="login-brand">
          <div className="brand-icon">
            <span>R</span>
          </div>

          <div>
            <h1>RBAC Manager</h1>
            <p>IDENTITY & ACCESS MANAGEMENT</p>
          </div>
        </div>

        <div className="login-heading">
          <h2>Bem-vindo de volta</h2>
          <p>Acesse sua conta para continuar</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label htmlFor="matricula">Matrícula</label>

            <input
              id="matricula"
              type="text"
              placeholder="Digite sua matrícula"
              autoComplete="username"
              value={matricula}
              disabled={carregando}
              onChange={(event) => {
                setMatricula(event.target.value)
                setErros((estadoAtual) => ({
                  ...estadoAtual,
                  matricula: '',
                }))
                setMensagem('')
              }}
              aria-invalid={Boolean(erros.matricula)}
              aria-describedby={erros.matricula ? 'erro-matricula' : undefined}
            />

            {erros.matricula && (
              <span id="erro-matricula" className="error-message">
                {erros.matricula}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>

            <div className="password-wrapper">
              <input
                id="senha"
                type={mostrarSenha ? 'text' : 'password'}
                placeholder="Digite sua senha"
                autoComplete="current-password"
                value={senha}
                disabled={carregando}
                onChange={(event) => {
                  setSenha(event.target.value)
                  setErros((estadoAtual) => ({
                    ...estadoAtual,
                    senha: '',
                  }))
                  setMensagem('')
                }}
                aria-invalid={Boolean(erros.senha)}
                aria-describedby={erros.senha ? 'erro-senha' : undefined}
              />

              <button
                type="button"
                className="toggle-password"
                onClick={() => setMostrarSenha(!mostrarSenha)}
                aria-label={mostrarSenha ? 'Ocultar senha' : 'Mostrar senha'}
                aria-pressed={mostrarSenha}
                disabled={carregando}
              >
                {mostrarSenha ? (
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      d="M3 3l18 18M10.6 10.6a2 2 0 002.8 2.8M9.9 5.2A11.5 11.5 0 0112 5c5 0 9 5 9 7s-4 7-9 7a9.8 9.8 0 01-4.1-.9M6.2 6.2C3.6 7.8 3 10.2 3 12c0 1.1.8 2.6 2.1 4"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      d="M2.5 12s3.5-7 9.5-7 9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7z"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <circle
                      cx="12"
                      cy="12"
                      r="3"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.7"
                    />
                  </svg>
                )}
              </button>
            </div>

            {erros.senha && (
              <span id="erro-senha" className="error-message">
                {erros.senha}
              </span>
            )}
          </div>

          <button type="submit" disabled={carregando}>
            {carregando ? 'Autenticando...' : 'Entrar'}
          </button>
        </form>

        {mensagem && (
          <p className="login-message" role="status" aria-live="polite">
            {mensagem}
          </p>
        )}

        <footer className="login-footer">
          Plataforma de Gerenciamento de Acessos
        </footer>
      </section>
    </main>
  )
}

export default Login
