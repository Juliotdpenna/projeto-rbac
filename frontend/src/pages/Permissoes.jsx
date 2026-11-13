
import { useEffect, useState } from 'react'
import { fazerRequisicao } from '../services/api'
import './Permissoes.css'

function Permissoes({ usuario, onLogout, onNavigate }) {
  const [permissoes, setPermissoes] = useState([])
  const [busca, setBusca] = useState('')
  const [filtroStatus, setFiltroStatus] = useState('todas')
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [permissaoEmAlteracao, setPermissaoEmAlteracao] = useState(null)
  const [mensagemSucesso, setMensagemSucesso] = useState('')
  const [permissaoEditando, setPermissaoEditando] = useState(null)

  const [formulario, setFormulario] = useState({
    nome: '',
    descricao: '',
  })

  async function atualizarTabela() {
    const dados = await fazerRequisicao('/permissoes')
    setPermissoes(dados)
  }

  useEffect(() => {
    let componenteAtivo = true

    async function carregarPermissoes() {
      try {
        const dados = await fazerRequisicao('/permissoes')

        if (componenteAtivo) {
          setPermissoes(dados)
        }
      } catch (erroAPI) {
        if (componenteAtivo) {
          setErro(erroAPI.message)
        }
      } finally {
        if (componenteAtivo) {
          setCarregando(false)
        }
      }
    }

    carregarPermissoes()

    return () => {
      componenteAtivo = false
    }
  }, [])

  function handleFormulario(evento) {
    const { name, value } = evento.target

    setFormulario((estadoAnterior) => ({
      ...estadoAnterior,
      [name]: value,
    }))
  }

  function abrirFormulario() {
    setPermissaoEditando(null)
    setFormulario({ nome: '', descricao: '' })
    setErro('')
    setMensagemSucesso('')
    setMostrarFormulario(true)
  }

  function abrirEdicao(permissao) {
    setPermissaoEditando(permissao)
    setFormulario({
      nome: permissao.nome,
      descricao: permissao.descricao,
    })
    setErro('')
    setMensagemSucesso('')
    setMostrarFormulario(true)
  }

  function cancelarFormulario() {
    setMostrarFormulario(false)
    setPermissaoEditando(null)
    setFormulario({ nome: '', descricao: '' })
    setErro('')
  }

  async function salvarPermissao(evento) {
    evento.preventDefault()

    const nome = formulario.nome.trim()
    const descricao = formulario.descricao.trim()

    if (!nome || !descricao) {
      setErro('Preencha todos os campos antes de continuar.')
      return
    }

    setSalvando(true)
    setErro('')
    setMensagemSucesso('')

    const estavaEditando = Boolean(permissaoEditando)

    try {
      if (estavaEditando) {
        await fazerRequisicao(
          `/permissoes/${permissaoEditando.id}`,
          {
            method: 'PUT',
            body: JSON.stringify({ nome, descricao }),
          }
        )
      } else {
        await fazerRequisicao('/permissoes', {
          method: 'POST',
          body: JSON.stringify({
            nome,
            descricao,
            status: true,
          }),
        })
      }

      setMostrarFormulario(false)
      setPermissaoEditando(null)
      setFormulario({ nome: '', descricao: '' })

      setMensagemSucesso(
        estavaEditando
          ? 'Permissão atualizada com sucesso!'
          : 'Permissão cadastrada com sucesso!'
      )

      try {
        await atualizarTabela()
      } catch {
        setErro(
          'Operação realizada, mas não foi possível atualizar a tabela. Recarregue a página.'
        )
      }
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setSalvando(false)
    }
  }

  async function alterarStatusPermissao(permissao) {
    const acao = permissao.status ? 'desativar' : 'reativar'

    if (
      permissao.status &&
      !window.confirm(
        `Deseja realmente desativar a permissão "${permissao.nome}"?`
      )
    ) {
      return
    }

    setPermissaoEmAlteracao(permissao.id)
    setErro('')
    setMensagemSucesso('')

    try {
      if (permissao.status) {
        await fazerRequisicao(`/permissoes/${permissao.id}`, {
          method: 'DELETE',
        })
      } else {
        await fazerRequisicao(
          `/permissoes/${permissao.id}/reativar`,
          {
            method: 'PATCH',
          }
        )
      }

      setMensagemSucesso(
        `Permissão "${permissao.nome}" ${acao} com sucesso!`
      )

      await atualizarTabela()
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setPermissaoEmAlteracao(null)
    }
  }

  const permissoesFiltradas = permissoes.filter((permissao) => {
    const correspondeBusca = permissao.nome
      .toLowerCase()
      .includes(busca.toLowerCase())

    const correspondeStatus =
      filtroStatus === 'todas' ||
      (filtroStatus === 'ativas' && permissao.status) ||
      (filtroStatus === 'inativas' && !permissao.status)

    return correspondeBusca && correspondeStatus
  })

  return (
    <div className="dashboard-container">
      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">
          <div className="brand-icon">R</div>
          <div>
            <h1>RBAC Manager</h1>
            <p>IDENTITY & ACCESS MANAGEMENT</p>
          </div>
        </div>

        <nav className="dashboard-navigation">
          <span className="navigation-label">MENU PRINCIPAL</span>

          <button
            className="navigation-item"
            onClick={() => onNavigate('dashboard')}
          >
            Dashboard
          </button>

          <button
            className="navigation-item"
            onClick={() => onNavigate('usuarios')}
          >
            Usuários
          </button>

          <button
            className="navigation-item"
            onClick={() => onNavigate('roles')}
          >
            Roles
          </button>

          <button
            className="navigation-item active"
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

      <main className="dashboard-content">
        <header className="dashboard-header">
          <div>
            <span className="page-overline">CONTROLE DE ACESSO</span>
            <h2>Permissões</h2>
          </div>

          <div className="user-identification">
            <div className="user-avatar">
              {usuario.nome.charAt(0).toUpperCase()}
            </div>
            <span>{usuario.nome}</span>
          </div>
        </header>

        <section className="users-section">
          <div className="users-heading">
            <div>
              <h3>Gerenciamento de Permissões</h3>
              <p>
                Consulte e gerencie as permissões cadastradas na plataforma.
              </p>
            </div>

            <div className="users-heading-actions">
              <span className="users-total">
                {permissoes.length} permissões cadastradas
              </span>

              <button
                className="new-user-button"
                type="button"
                onClick={abrirFormulario}
              >
                + Nova Permissão
              </button>
            </div>
          </div>

          {mostrarFormulario && (
            <form className="user-form" onSubmit={salvarPermissao}>
              <h3>
                {permissaoEditando
                  ? 'Editar Permissão'
                  : 'Cadastro de Permissão'}
              </h3>

              <p>
                {permissaoEditando
                  ? 'Altere o nome ou a descrição desta permissão.'
                  : 'Informe os dados da nova permissão de acesso.'}
              </p>

              <div className="user-form-grid">
                <label>
                  Nome da Permissão
                  <input
                    type="text"
                    name="nome"
                    value={formulario.nome}
                    onChange={handleFormulario}
                    placeholder="Ex.: VISUALIZAR_RELATORIOS"
                    maxLength={100}
                    required
                  />
                </label>

                <label>
                  Descrição
                  <input
                    type="text"
                    name="descricao"
                    value={formulario.descricao}
                    onChange={handleFormulario}
                    placeholder="Descreva a finalidade desta permissão"
                    maxLength={255}
                    required
                  />
                </label>
              </div>

              {!permissaoEditando && (
                <p className="user-form-hint">
                  A nova permissão será cadastrada com status ativo.
                </p>
              )}

              {erro && <div className="users-error">{erro}</div>}

              <div className="user-form-actions">
                <button
                  className="cancel-user-button"
                  type="button"
                  onClick={cancelarFormulario}
                  disabled={salvando}
                >
                  Cancelar
                </button>

                <button
                  className="save-user-button"
                  type="submit"
                  disabled={salvando}
                >
                  {salvando
                    ? 'Salvando...'
                    : permissaoEditando
                      ? 'Salvar alterações'
                      : 'Cadastrar Permissão'}
                </button>
              </div>
            </form>
          )}

          {mensagemSucesso && (
            <div className="users-success">{mensagemSucesso}</div>
          )}

          {erro && !mostrarFormulario && (
            <div className="users-error">{erro}</div>
          )}

          <div className="users-filters">
            <input
              type="text"
              placeholder="Pesquisar permissão pelo nome..."
              value={busca}
              onChange={(evento) => setBusca(evento.target.value)}
            />

            <select
              value={filtroStatus}
              onChange={(evento) => setFiltroStatus(evento.target.value)}
            >
              <option value="todas">Todos os status</option>
              <option value="ativas">Ativas</option>
              <option value="inativas">Inativas</option>
            </select>
          </div>

          {carregando && (
            <div className="users-feedback">
              Carregando permissões...
            </div>
          )}

          {!carregando && (
            <div className="users-table-container">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>NOME</th>
                    <th>DESCRIÇÃO</th>
                    <th>STATUS</th>
                    <th>AÇÕES</th>
                  </tr>
                </thead>

                <tbody>
                  {permissoesFiltradas.map((permissao) => (
                    <tr key={permissao.id}>
                      <td>{permissao.id}</td>
                      <td>{permissao.nome}</td>
                      <td>{permissao.descricao}</td>
                      <td>
                        <span
                          className={`user-status ${
                            permissao.status ? 'active' : 'inactive'
                          }`}
                        >
                          {permissao.status ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td>
                        <div className="user-actions">
                          <button
                            className="edit-user-button"
                            type="button"
                            onClick={() => abrirEdicao(permissao)}
                          >
                            Editar
                          </button>

                          <button
                            className={
                              permissao.status
                                ? 'deactivate-user-button'
                                : 'activate-user-button'
                            }
                            type="button"
                            disabled={
                              permissaoEmAlteracao === permissao.id
                            }
                            onClick={() =>
                              alterarStatusPermissao(permissao)
                            }
                          >
                            {permissaoEmAlteracao === permissao.id
                              ? 'Aguarde...'
                              : permissao.status
                                ? 'Desativar'
                                : 'Reativar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}

                  {permissoesFiltradas.length === 0 && (
                    <tr>
                      <td colSpan="5" className="users-feedback">
                        Nenhuma permissão encontrada.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default Permissoes
