import { useEffect, useState } from 'react'
import { fazerRequisicao } from '../services/api'
import './Dashboard.css'

function Dashboard({ usuario, onLogout, onNavigate }) {
  const [indicadores, setIndicadores] = useState({
    usuarios: null,
    roles: null,
    permissoes: null,
    grupos: null,
  })

  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    let componenteAtivo = true

    async function carregarIndicadores() {
      const consultas = [
        { chave: 'usuarios', endpoint: '/usuarios' },
        { chave: 'roles', endpoint: '/roles' },
        { chave: 'permissoes', endpoint: '/permissoes' },
        { chave: 'grupos', endpoint: '/grupos' },
      ]

      const resultados = await Promise.allSettled(
        consultas.map(({ endpoint }) => fazerRequisicao(endpoint))
      )

      if (!componenteAtivo) {
        return
      }

      const novosIndicadores = {}

      resultados.forEach((resultado, indice) => {
        const chave = consultas[indice].chave

        if (resultado.status === 'fulfilled') {
          novosIndicadores[chave] = {
            valor: resultado.value.length,
            erro: null,
          }
        } else {
          novosIndicadores[chave] = {
            valor: null,
            erro: resultado.reason.message,
          }
        }
      })

      setIndicadores(novosIndicadores)
      setCarregando(false)
    }

    carregarIndicadores()

    return () => {
      componenteAtivo = false
    }
  }, [])

  const cards = [
    { chave: 'usuarios', titulo: 'Usuários' },
    { chave: 'roles', titulo: 'Roles' },
    { chave: 'permissoes', titulo: 'Permissões' },
    { chave: 'grupos', titulo: 'Grupos' },
  ]

  return (
    <main className="dashboard-container">
      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">
          <div className="brand-icon">
            <span>R</span>
          </div>

          <div>
            <h1>RBAC Manager</h1>
            <p>IDENTITY & ACCESS MANAGEMENT</p>
          </div>
        </div>

        <nav className="dashboard-navigation" aria-label="Menu principal">
          <span className="navigation-label">MENU PRINCIPAL</span>

          <button className="navigation-item active" type="button">
            Dashboard
          </button>

          <button
            className="navigation-item"
            type="button"
            onClick={() => onNavigate('usuarios')}
          >
            Usuários
          </button>

          <button
            className="navigation-item"
            type="button"
            onClick={() => onNavigate('roles')}
          >
            Roles
          </button>

          <button
            className="navigation-item"
            type="button"
            onClick={() => onNavigate('permissoes')}
          >
            Permissões
          </button>

          <button
            className="navigation-item"
            type="button"
            onClick={() => onNavigate('grupos')}
          >
            Grupos
          </button>
          </nav>

        <div className="sidebar-footer">
          <span>Conectado como</span>
          <strong>{usuario.nome}</strong>

          <button
            className="logout-button"
            type="button"
            onClick={onLogout}
          >
            Sair da conta
          </button>
        </div>
      </aside>

      <section className="dashboard-content">
        <header className="dashboard-header">
          <div>
            <span className="page-overline">VISÃO GERAL</span>
            <h2>Dashboard</h2>
          </div>

          <div className="user-identification">
            <span>{usuario.nome}</span>
            <span className="user-avatar">
              {usuario.nome.charAt(0).toUpperCase()}
            </span>
          </div>
        </header>

        <section className="welcome-section">
          <span className="welcome-label">AMBIENTE DE GERENCIAMENTO</span>
          <h3>Bem-vindo, {usuario.nome}!</h3>
          <p>
            Gerencie identidades, funções e permissões em um único ambiente.
          </p>
        </section>

        <section className="dashboard-section">
          <div className="section-heading">
            <h3>Visão geral do sistema</h3>
            <p>Total de registros cadastrados na plataforma</p>
          </div>

          <div className="dashboard-cards">
            {cards.map((card) => {
              const indicador = indicadores[card.chave]

              return (
                <article
                  className="dashboard-stat-card"
                  key={card.chave}
                >
                  <span>{card.titulo}</span>

                  <strong>
                    {carregando
                      ? '...'
                      : indicador?.valor ?? '—'}
                  </strong>

                  <p>
                    {carregando
                      ? 'Carregando dados...'
                      : indicador?.erro
                        ? 'Não foi possível consultar'
                        : 'Registros cadastrados'}
                  </p>
                </article>
              )
            })}
          </div>
        </section>
      </section>
    </main>
  )
}

export default Dashboard
