
import { useEffect, useState } from 'react'
import { fazerRequisicao } from '../services/api'
import './Grupos.css'

const formularioInicial = {
  nome: '',
  descricao: '',
}

function Grupos({ usuario, onLogout, onNavigate }) {
  const [grupos, setGrupos] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [pesquisa, setPesquisa] = useState('')
  const [filtroStatus, setFiltroStatus] = useState('todos')

  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [mensagem, setMensagem] = useState('')
  const [erroFormulario, setErroFormulario] = useState('')
  const [grupoEditando, setGrupoEditando] = useState(null)
  const [grupoEmAlteracao, setGrupoEmAlteracao] = useState(null)

  const [formulario, setFormulario] = useState(formularioInicial)

  // Estados do gerenciamento de associações
  const [grupoSelecionado, setGrupoSelecionado] = useState(null)
  const [usuariosDisponiveis, setUsuariosDisponiveis] = useState([])
  const [rolesDisponiveis, setRolesDisponiveis] = useState([])
  const [carregandoAssociacoes, setCarregandoAssociacoes] = useState(false)
  const [itemEmAlteracao, setItemEmAlteracao] = useState(null)

  useEffect(() => {
    let componenteAtivo = true

    async function carregarGrupos() {
      try {
        const dados = await fazerRequisicao('/grupos')

        if (componenteAtivo) {
          setGrupos(dados)
        }
      } catch (erroConsulta) {
        if (componenteAtivo) {
          setErro(erroConsulta.message)
        }
      } finally {
        if (componenteAtivo) {
          setCarregando(false)
        }
      }
    }

    carregarGrupos()

    return () => {
      componenteAtivo = false
    }
  }, [])

  // Atualiza a tabela de grupos
  async function atualizarTabela() {
    const dados = await fazerRequisicao('/grupos')
    setGrupos(dados)
  }

  // Carrega os dados necessários para gerenciar um grupo
  async function carregarAssociacoes(grupo) {
    setGrupoSelecionado(grupo)
    setCarregandoAssociacoes(true)
    setErro('')
    setMensagem('')

    try {
      const [dadosGrupo, usuarios, roles] = await Promise.all([
        fazerRequisicao(`/grupos/${grupo.id}`),
        fazerRequisicao('/usuarios'),
        fazerRequisicao('/roles'),
      ])

      setGrupoSelecionado(dadosGrupo)
      setUsuariosDisponiveis(usuarios)
      setRolesDisponiveis(roles)
    } catch (erroAPI) {
      setErro(erroAPI.message)
      setGrupoSelecionado(null)
    } finally {
      setCarregandoAssociacoes(false)
    }
  }

  // Adiciona ou remove um usuário do grupo
  async function alterarAssociacaoUsuario(usuarioItem, associado) {
    const identificador = `usuario-${usuarioItem.id}`

    setItemEmAlteracao(identificador)
    setErro('')
    setMensagem('')

    try {
      const endpoint = `/grupos/${grupoSelecionado.id}/usuarios/${usuarioItem.id}`

      await fazerRequisicao(endpoint, {
        method: associado ? 'DELETE' : 'POST',
      })

      const dadosGrupo = await fazerRequisicao(
        `/grupos/${grupoSelecionado.id}`
      )

      setGrupoSelecionado(dadosGrupo)
      await atualizarTabela()

      setMensagem(
        associado
          ? 'Usuário removido do grupo com sucesso!'
          : 'Usuário associado ao grupo com sucesso!'
      )
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setItemEmAlteracao(null)
    }
  }

  // Adiciona ou remove uma Role do grupo
  async function alterarAssociacaoRole(roleItem, associado) {
    const identificador = `role-${roleItem.id}`

    setItemEmAlteracao(identificador)
    setErro('')
    setMensagem('')

    try {
      const endpoint = `/grupos/${grupoSelecionado.id}/roles/${roleItem.id}`

      await fazerRequisicao(endpoint, {
        method: associado ? 'DELETE' : 'POST',
      })

      const dadosGrupo = await fazerRequisicao(
        `/grupos/${grupoSelecionado.id}`
      )

      setGrupoSelecionado(dadosGrupo)
      await atualizarTabela()

      setMensagem(
        associado
          ? 'Role removida do grupo com sucesso!'
          : 'Role associada ao grupo com sucesso!'
      )
    } catch (erroAPI) {
      setErro(erroAPI.message)
    } finally {
      setItemEmAlteracao(null)
    }
  }

  function atualizarCampo(evento) {
    const { name, value } = evento.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  function abrirCadastro() {
    setGrupoEditando(null)
    setFormulario(formularioInicial)
    setErroFormulario('')
    setMensagem('')
    setErro('')
    setMostrarFormulario(true)
  }

  function abrirEdicao(grupo) {
    setGrupoEditando(grupo)
    setFormulario({
      nome: grupo.nome,
      descricao: grupo.descricao,
    })
    setErroFormulario('')
    setMensagem('')
    setErro('')
    setMostrarFormulario(true)
  }

  function fecharFormulario() {
    setMostrarFormulario(false)
    setGrupoEditando(null)
    setFormulario(formularioInicial)
    setErroFormulario('')
  }

  async function salvarGrupo(evento) {
    evento.preventDefault()

    const nome = formulario.nome.trim()
    const descricao = formulario.descricao.trim()

    if (!nome || !descricao) {
      setErroFormulario('Preencha todos os campos antes de continuar.')
      return
    }

    setSalvando(true)
    setErroFormulario('')
    setMensagem('')
    setErro('')

    const estavaEditando = Boolean(grupoEditando)

    try {
      if (estavaEditando) {
        await fazerRequisicao(`/grupos/${grupoEditando.id}`, {
          method: 'PUT',
          body: JSON.stringify({ nome, descricao }),
        })
      } else {
        await fazerRequisicao('/grupos', {
          method: 'POST',
          body: JSON.stringify({
            nome,
            descricao,
            status: true,
          }),
        })
      }

      fecharFormulario()

      setMensagem(
        estavaEditando
          ? 'Grupo atualizado com sucesso!'
          : 'Grupo cadastrado com sucesso!'
      )

      try {
        await atualizarTabela()
      } catch {
        setErro(
          'Operação realizada, mas não foi possível atualizar a tabela. Recarregue a página.'
        )
      }
    } catch (erroRequisicao) {
      setErroFormulario(erroRequisicao.message)
    } finally {
      setSalvando(false)
    }
  }

  async function alterarStatusGrupo(grupo) {
    const acao = grupo.status ? 'desativar' : 'reativar'

    if (
      grupo.status &&
      !window.confirm(
        `Deseja realmente desativar o grupo "${grupo.nome}"?`
      )
    ) {
      return
    }

    setGrupoEmAlteracao(grupo.id)
    setErro('')
    setMensagem('')

    try {
      const endpoint = grupo.status
        ? `/grupos/${grupo.id}`
        : `/grupos/${grupo.id}/reativar`

      await fazerRequisicao(endpoint, {
        method: grupo.status ? 'DELETE' : 'PATCH',
      })

      setMensagem(`Grupo "${grupo.nome}" ${acao} com sucesso!`)

      if (grupoSelecionado?.id === grupo.id && grupo.status) {
        setGrupoSelecionado(null)
      }

      await atualizarTabela()
    } catch (erroRequisicao) {
      setErro(erroRequisicao.message)
    } finally {
      setGrupoEmAlteracao(null)
    }
  }

  const gruposFiltrados = grupos.filter((grupo) => {
    const termo = pesquisa.toLowerCase()

    const correspondePesquisa =
      grupo.nome.toLowerCase().includes(termo) ||
      grupo.descricao.toLowerCase().includes(termo)

    const correspondeStatus =
      filtroStatus === 'todos' ||
      (filtroStatus === 'ativos' && grupo.status) ||
      (filtroStatus === 'inativos' && !grupo.status)

    return correspondePesquisa && correspondeStatus
  })

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

          <button
            className="navigation-item"
            type="button"
            onClick={() => onNavigate('dashboard')}
          >
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

          <button className="navigation-item active" type="button">
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
            <span className="page-overline">CONTROLE DE ACESSO</span>
            <h2>Grupos</h2>
          </div>

          <div className="user-identification">
            <span>{usuario.nome}</span>
            <span className="user-avatar">
              {usuario.nome.charAt(0).toUpperCase()}
            </span>
          </div>
        </header>

        <section className="users-section">
          <div className="users-heading">
            <div>
              <h3>Gerenciamento de grupos</h3>
              <p>
                Organize usuários e Roles em grupos de acesso.
              </p>
            </div>

            <div className="users-heading-actions">
              <span className="users-total">
                {grupos.length} grupos cadastrados
              </span>

              <button
                className="new-user-button"
                type="button"
                onClick={abrirCadastro}
              >
                + Novo grupo
              </button>
            </div>
          </div>

          {mensagem && (
            <p className="users-success" role="status">
              {mensagem}
            </p>
          )}

          {erro && (
            <p className="users-error" role="alert">
              {erro}
            </p>
          )}

          {mostrarFormulario && (
            <form className="user-form" onSubmit={salvarGrupo}>
              <h3>
                {grupoEditando ? 'Editar grupo' : 'Novo grupo'}
              </h3>

              <p>
                Informe o nome e a finalidade do grupo.
              </p>

              <div className="user-form-grid">
                <label>
                  Nome do grupo
                  <input
                    type="text"
                    name="nome"
                    value={formulario.nome}
                    onChange={atualizarCampo}
                    placeholder="Ex.: GRUPO_TI"
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
                    onChange={atualizarCampo}
                    placeholder="Descreva a finalidade do grupo"
                    maxLength={255}
                    required
                  />
                </label>
              </div>

              {!grupoEditando && (
                <p className="user-form-hint">
                  O novo grupo será cadastrado com status ativo.
                </p>
              )}

              {erroFormulario && (
                <p className="users-error" role="alert">
                  {erroFormulario}
                </p>
              )}

              <div className="user-form-actions">
                <button
                  type="button"
                  className="cancel-user-button"
                  onClick={fecharFormulario}
                  disabled={salvando}
                >
                  Cancelar
                </button>

                <button
                  type="submit"
                  className="save-user-button"
                  disabled={salvando}
                >
                  {salvando
                    ? 'Salvando...'
                    : grupoEditando
                      ? 'Salvar alterações'
                      : 'Cadastrar grupo'}
                </button>
              </div>
            </form>
          )}

          <div className="users-filters">
            <input
              type="search"
              placeholder="Pesquisar por nome ou descrição..."
              value={pesquisa}
              onChange={(evento) => setPesquisa(evento.target.value)}
              aria-label="Pesquisar grupos"
            />

            <select
              value={filtroStatus}
              onChange={(evento) => setFiltroStatus(evento.target.value)}
              aria-label="Filtrar grupos por status"
            >
              <option value="todos">Todos os status</option>
              <option value="ativos">Ativos</option>
              <option value="inativos">Inativos</option>
            </select>
          </div>

          {carregando && (
            <p className="users-feedback">Carregando grupos...</p>
          )}

          {!carregando && !erro && (
            <div className="users-table-container">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Usuários</th>
                    <th>Roles</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>

                <tbody>
                  {gruposFiltrados.map((grupo) => (
                    <tr key={grupo.id}>
                      <td>{grupo.id}</td>
                      <td>{grupo.nome}</td>
                      <td>{grupo.descricao}</td>
                      <td>{grupo.usuarios.length}</td>
                      <td>{grupo.roles.length}</td>
                      <td>
                        <span
                          className={`user-status ${
                            grupo.status ? 'active' : 'inactive'
                          }`}
                        >
                          {grupo.status ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td>
                        <div className="user-actions">
                          <button
                            className="edit-user-button"
                            type="button"
                            onClick={() => abrirEdicao(grupo)}
                          >
                            Editar
                          </button>

                          <button
                            className="edit-user-button"
                            type="button"
                            onClick={() => carregarAssociacoes(grupo)}
                            disabled={!grupo.status}
                          >
                            Gerenciar
                          </button>

                          <button
                            className={
                              grupo.status
                                ? 'deactivate-user-button'
                                : 'activate-user-button'
                            }
                            type="button"
                            disabled={grupoEmAlteracao === grupo.id}
                            onClick={() => alterarStatusGrupo(grupo)}
                          >
                            {grupoEmAlteracao === grupo.id
                              ? 'Aguarde...'
                              : grupo.status
                                ? 'Desativar'
                                : 'Reativar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}

                  {gruposFiltrados.length === 0 && (
                    <tr>
                      <td colSpan="7" className="users-feedback">
                        Nenhum grupo encontrado.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {grupoSelecionado && (
            <section className="user-form">
              <div className="users-heading">
                <div>
                  <h3>Gerenciar grupo: {grupoSelecionado.nome}</h3>
                  <p>Associe usuários e Roles a este grupo.</p>
                </div>

                <button
                  type="button"
                  className="cancel-user-button"
                  onClick={() => setGrupoSelecionado(null)}
                >
                  Fechar
                </button>
              </div>

              {carregandoAssociacoes ? (
                <p className="users-feedback">
                  Carregando associações...
                </p>
              ) : (
                <>
                  {/* Gerenciamento de usuários */}
                  <div className="user-form-grid">
                    <div>
                      <h4>Usuários associados</h4>

                      {grupoSelecionado.usuarios.length === 0 ? (
                        <p className="users-feedback">
                          Nenhum usuário associado a este grupo.
                        </p>
                      ) : (
                        grupoSelecionado.usuarios.map((usuarioItem) => (
                          <div
                            key={usuarioItem.id}
                            className="user-actions"
                          >
                            <span>{usuarioItem.nome}</span>

                            <button
                              type="button"
                              className="deactivate-user-button"
                              disabled={
                                itemEmAlteracao === `usuario-${usuarioItem.id}`
                              }
                              onClick={() =>
                                alterarAssociacaoUsuario(usuarioItem, true)
                              }
                            >
                              {itemEmAlteracao === `usuario-${usuarioItem.id}`
                                ? 'Aguarde...'
                                : 'Remover'}
                            </button>
                          </div>
                        ))
                      )}
                    </div>

                    <div>
                      <h4>Adicionar usuários</h4>

                      {usuariosDisponiveis
                        .filter(
                          (usuarioItem) =>
                            usuarioItem.status &&
                            !grupoSelecionado.usuarios.some(
                              (associado) => associado.id === usuarioItem.id
                            )
                        )
                        .map((usuarioItem) => (
                          <div
                            key={usuarioItem.id}
                            className="user-actions"
                          >
                            <span>{usuarioItem.nome}</span>

                            <button
                              type="button"
                              className="activate-user-button"
                              disabled={
                                itemEmAlteracao === `usuario-${usuarioItem.id}`
                              }
                              onClick={() =>
                                alterarAssociacaoUsuario(usuarioItem, false)
                              }
                            >
                              {itemEmAlteracao === `usuario-${usuarioItem.id}`
                                ? 'Aguarde...'
                                : 'Adicionar'}
                            </button>
                          </div>
                        ))}

                      {usuariosDisponiveis.filter(
                        (usuarioItem) =>
                          usuarioItem.status &&
                          !grupoSelecionado.usuarios.some(
                            (associado) => associado.id === usuarioItem.id
                          )
                      ).length === 0 && (
                        <p className="users-feedback">
                          Não há usuários ativos disponíveis para adicionar.
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Gerenciamento de Roles */}
                  <div className="user-form-grid">
                    <div>
                      <h4>Roles associadas</h4>

                      {grupoSelecionado.roles.length === 0 ? (
                        <p className="users-feedback">
                          Nenhuma Role associada a este grupo.
                        </p>
                      ) : (
                        grupoSelecionado.roles.map((roleItem) => (
                          <div
                            key={roleItem.id}
                            className="user-actions"
                          >
                            <span>{roleItem.nome}</span>

                            <button
                              type="button"
                              className="deactivate-user-button"
                              disabled={
                                itemEmAlteracao === `role-${roleItem.id}`
                              }
                              onClick={() =>
                                alterarAssociacaoRole(roleItem, true)
                              }
                            >
                              {itemEmAlteracao === `role-${roleItem.id}`
                                ? 'Aguarde...'
                                : 'Remover'}
                            </button>
                          </div>
                        ))
                      )}
                    </div>

                    <div>
                      <h4>Adicionar Roles</h4>

                      {rolesDisponiveis
                        .filter(
                          (roleItem) =>
                            roleItem.status &&
                            !grupoSelecionado.roles.some(
                              (associada) => associada.id === roleItem.id
                            )
                        )
                        .map((roleItem) => (
                          <div
                            key={roleItem.id}
                            className="user-actions"
                          >
                            <span>{roleItem.nome}</span>

                            <button
                              type="button"
                              className="activate-user-button"
                              disabled={
                                itemEmAlteracao === `role-${roleItem.id}`
                              }
                              onClick={() =>
                                alterarAssociacaoRole(roleItem, false)
                              }
                            >
                              {itemEmAlteracao === `role-${roleItem.id}`
                                ? 'Aguarde...'
                                : 'Adicionar'}
                            </button>
                          </div>
                        ))}

                      {rolesDisponiveis.filter(
                        (roleItem) =>
                          roleItem.status &&
                          !grupoSelecionado.roles.some(
                            (associada) => associada.id === roleItem.id
                          )
                      ).length === 0 && (
                        <p className="users-feedback">
                          Não há Roles ativas disponíveis para adicionar.
                        </p>
                      )}
                    </div>
                  </div>
                </>
              )}
            </section>
          )}
        </section>
      </section>
    </main>
  )
}

export default Grupos
