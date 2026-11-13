import { useEffect, useState } from 'react'
import { fazerRequisicao } from '../services/api'
import './Roles.css'

function Roles({ usuario, onLogout, onNavigate }) {
  const [roles, setRoles] = useState([])
  const [busca, setBusca] = useState('')
  const [filtroStatus, setFiltroStatus] = useState('todas')
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [roleEmAlteracao, setRoleEmAlteracao] = useState(null)
  const [mensagemSucesso, setMensagemSucesso] = useState('')
  const [roleEditando, setRoleEditando] = useState(null)

  const [roleSelecionada, setRoleSelecionada] = useState(null)
  const [permissoesRole, setPermissoesRole] = useState([])
  const [permissoesDisponiveis, setPermissoesDisponiveis] = useState([])
  const [carregandoPermissoes, setCarregandoPermissoes] = useState(false)
  const [permissaoEmAlteracao, setPermissaoEmAlteracao] = useState(null)

  const [formulario, setFormulario] = useState({
    nome: '',
    descricao: '',
  })

  async function atualizarTabela() {
    const dados = await fazerRequisicao('/roles')
    setRoles(dados)
  }

  async function carregarPermissoes(role) {
    setRoleSelecionada(role)
    setCarregandoPermissoes(true)
    setErro('')
    setMensagemSucesso('')

    try {
      const [associadas, disponiveis] = await Promise.all([
        fazerRequisicao(`/roles/${role.id}/permissoes`),
        fazerRequisicao('/permissoes'),
      ])

      setPermissoesRole(associadas)
      setPermissoesDisponiveis(disponiveis)
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setCarregandoPermissoes(false)
    }
  }

  useEffect(() => {
    let componenteAtivo = true

    async function carregarRoles() {
      try {
        const dados = await fazerRequisicao('/roles')

        if (componenteAtivo) {
          setRoles(dados)
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

    carregarRoles()

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
    setRoleEditando(null)
    setFormulario({ nome: '', descricao: '' })
    setErro('')
    setMensagemSucesso('')
    setMostrarFormulario(true)
    setRoleSelecionada(null)
  }

  function abrirEdicao(role) {
    setRoleEditando(role)
    setFormulario({
      nome: role.nome,
      descricao: role.descricao,
    })
    setErro('')
    setMensagemSucesso('')
    setMostrarFormulario(true)
    setRoleSelecionada(null)
  }

  function cancelarFormulario() {
    setMostrarFormulario(false)
    setRoleEditando(null)
    setFormulario({ nome: '', descricao: '' })
    setErro('')
  }

  async function salvarRole(evento) {
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

    const estavaEditando = Boolean(roleEditando)

    try {
      if (estavaEditando) {
        await fazerRequisicao(`/roles/${roleEditando.id}`, {
          method: 'PUT',
          body: JSON.stringify({ nome, descricao }),
        })
      } else {
        await fazerRequisicao('/roles', {
          method: 'POST',
          body: JSON.stringify({ nome, descricao }),
        })
      }

      setMostrarFormulario(false)
      setRoleEditando(null)
      setFormulario({ nome: '', descricao: '' })
      setMensagemSucesso(
        estavaEditando
          ? 'Role atualizada com sucesso!'
          : 'Role cadastrada com sucesso!'
      )

      try {
        await atualizarTabela()
      } catch {
        setErro('Operação realizada, mas não foi possível atualizar a tabela. Recarregue a página.')
      }
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setSalvando(false)
    }
  }

  async function alterarStatusRole(role) {
    const acao = role.status ? 'desativar' : 'reativar'

    if (
      role.status &&
      !window.confirm(
        `Deseja realmente desativar a Role "${role.nome}"?`
      )
    ) {
      return
    }

    setRoleEmAlteracao(role.id)
    setErro('')
    setMensagemSucesso('')

    try {
      if (role.status) {
        await fazerRequisicao(`/roles/${role.id}`, {
          method: 'DELETE',
        })
      } else {
        await fazerRequisicao(`/roles/${role.id}/reativar`, {
          method: 'PATCH',
        })
      }

      setMensagemSucesso(`Role "${role.nome}" ${acao} com sucesso!`)
      await atualizarTabela()
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setRoleEmAlteracao(null)
    }
  }

  async function alterarAssociacaoPermissao(permissao) {
    const jaAssociada = permissoesRole.some(
      (item) => item.id === permissao.id
    )

    setPermissaoEmAlteracao(permissao.id)
    setErro('')
    setMensagemSucesso('')

    try {
      if (jaAssociada) {
        await fazerRequisicao(
          `/roles/${roleSelecionada.id}/permissoes/${permissao.id}`,
          { method: 'DELETE' }
        )
      } else {
        await fazerRequisicao(
          `/roles/${roleSelecionada.id}/permissoes/${permissao.id}`,
          { method: 'POST' }
        )
      }

      await carregarPermissoes(roleSelecionada)

      setMensagemSucesso(
        jaAssociada
          ? `Permissão "${permissao.nome}" removida da Role.`
          : `Permissão "${permissao.nome}" associada à Role.`
      )

      await atualizarTabela()
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setPermissaoEmAlteracao(null)
    }
  }

  const rolesFiltradas = roles.filter((role) => {
    const correspondeBusca = role.nome
      .toLowerCase()
      .includes(busca.toLowerCase())

    const correspondeStatus =
      filtroStatus === 'todas' ||
      (filtroStatus === 'ativas' && role.status) ||
      (filtroStatus === 'inativas' && !role.status)

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

          <button className="navigation-item active" type="button">
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

      <main className="dashboard-content">
        <header className="dashboard-header">
          <div>
            <span className="page-overline">CONTROLE DE ACESSO</span>
            <h2>Roles</h2>
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
              <h3>Gerenciamento de Roles</h3>
              <p>Consulte e gerencie as funções cadastradas na plataforma.</p>
            </div>

            <div className="users-heading-actions">
              <span className="users-total">
                {roles.length} Roles cadastradas
              </span>

              <button
                className="new-user-button"
                type="button"
                onClick={abrirFormulario}
              >
                + Nova Role
              </button>
            </div>
          </div>

          {mostrarFormulario && (
            <form className="user-form" onSubmit={salvarRole}>
              <h3>{roleEditando ? 'Editar Role' : 'Cadastro de Role'}</h3>

              <p>
                {roleEditando
                  ? 'Altere o nome ou a descrição desta Role.'
                  : 'Informe os dados da nova função de acesso.'}
              </p>

              <div className="user-form-grid">
                <label>
                  Nome da Role
                  <input
                    type="text"
                    name="nome"
                    value={formulario.nome}
                    onChange={handleFormulario}
                    placeholder="Ex.: ROLE_ANALISTA_TI"
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
                    placeholder="Descreva a finalidade desta Role"
                    maxLength={255}
                    required
                  />
                </label>
              </div>

              {!roleEditando && (
                <p className="user-form-hint">
                  A nova Role será cadastrada com status ativo.
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
                    : roleEditando
                      ? 'Salvar alterações'
                      : 'Cadastrar Role'}
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
              placeholder="Pesquisar Role pelo nome..."
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
            <div className="users-feedback">Carregando Roles...</div>
          )}

          {!carregando && (
            <div className="users-table-container">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>NOME</th>
                    <th>DESCRIÇÃO</th>
                    <th>PERMISSÕES</th>
                    <th>STATUS</th>
                    <th>AÇÕES</th>
                  </tr>
                </thead>

                <tbody>
                  {rolesFiltradas.map((role) => (
                    <tr key={role.id}>
                      <td>{role.id}</td>
                      <td>{role.nome}</td>
                      <td>{role.descricao}</td>
                      <td>{role.permissoes.length}</td>
                      <td>
                        <span
                          className={`user-status ${
                            role.status ? 'active' : 'inactive'
                          }`}
                        >
                          {role.status ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td>
                        <div className="user-actions">
                          <button
                            className="edit-user-button"
                            type="button"
                            onClick={() => abrirEdicao(role)}
                          >
                            Editar
                          </button>

                          <button
                            className="edit-user-button"
                            type="button"
                            disabled={!role.status}
                            onClick={() => carregarPermissoes(role)}
                          >
                            Permissões
                          </button>

                          <button
                            className={
                              role.status
                                ? 'deactivate-user-button'
                                : 'activate-user-button'
                            }
                            type="button"
                            disabled={roleEmAlteracao === role.id}
                            onClick={() => alterarStatusRole(role)}
                          >
                            {roleEmAlteracao === role.id
                              ? 'Aguarde...'
                              : role.status
                                ? 'Desativar'
                                : 'Reativar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}

                  {rolesFiltradas.length === 0 && (
                    <tr>
                      <td colSpan="6" className="users-feedback">
                        Nenhuma Role encontrada.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {roleSelecionada && (
            <div className="user-form">
              <div className="users-heading">
                <div>
                  <h3>Permissões da Role: {roleSelecionada.nome}</h3>
                  <p>
                    Associe ou remova permissões desta função de acesso.
                  </p>
                </div>

                <button
                  className="cancel-user-button"
                  type="button"
                  onClick={() => {
                    setRoleSelecionada(null)
                    setPermissoesRole([])
                    setErro('')
                  }}
                >
                  Fechar
                </button>
              </div>

              {carregandoPermissoes ? (
                <div className="users-feedback">
                  Carregando permissões...
                </div>
              ) : (
                <>
                  <h4>Permissões associadas</h4>

                  {permissoesRole.length === 0 ? (
                    <p>Esta Role ainda não possui permissões associadas.</p>
                  ) : (
                    <ul>
                      {permissoesRole.map((permissao) => (
                        <li key={permissao.id}>
                          <strong>{permissao.nome}</strong>
                          <span> — {permissao.descricao}</span>
                          <button
                            className="deactivate-user-button"
                            type="button"
                            disabled={permissaoEmAlteracao === permissao.id}
                            onClick={() =>
                              alterarAssociacaoPermissao(permissao)
                            }
                          >
                            {permissaoEmAlteracao === permissao.id
                              ? 'Aguarde...'
                              : 'Remover'}
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}

                  <h4>Adicionar permissão</h4>

                  {permissoesDisponiveis.filter(
                    (permissao) =>
                      permissao.status &&
                      !permissoesRole.some(
                        (associada) => associada.id === permissao.id
                      )
                  ).length === 0 ? (
                    <p>Não há permissões ativas disponíveis para adicionar.</p>
                  ) : (
                    <ul>
                      {permissoesDisponiveis
                        .filter(
                          (permissao) =>
                            permissao.status &&
                            !permissoesRole.some(
                              (associada) => associada.id === permissao.id
                            )
                        )
                        .map((permissao) => (
                          <li key={permissao.id}>
                            <strong>{permissao.nome}</strong>
                            <span> — {permissao.descricao}</span>
                            <button
                              className="activate-user-button"
                              type="button"
                              disabled={
                                permissaoEmAlteracao === permissao.id
                              }
                              onClick={() =>
                                alterarAssociacaoPermissao(permissao)
                              }
                            >
                              {permissaoEmAlteracao === permissao.id
                                ? 'Aguarde...'
                                : 'Adicionar'}
                            </button>
                          </li>
                        ))}
                    </ul>
                  )}
                </>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default Roles