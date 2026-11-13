
import { useEffect, useState } from 'react'
import { fazerRequisicao } from '../services/api'
import './Usuarios.css'

const formularioInicial = {
  nome: '',
  matricula: '',
  departamento: '',
  cargo: '',
  senha: '',
  confirmarSenha: '',
}

function Usuarios({ usuario, onLogout, onNavigate }) {
  const [usuarios, setUsuarios] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [pesquisa, setPesquisa] = useState('')
  const [filtroStatus, setFiltroStatus] = useState('todos')

  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [mensagem, setMensagem] = useState('')
  const [erroCadastro, setErroCadastro] = useState('')
  const [usuarioEditando, setUsuarioEditando] = useState(null)

  const [formulario, setFormulario] = useState(formularioInicial)

  useEffect(() => {
    let componenteAtivo = true

    async function carregarUsuarios() {
      try {
        const dados = await fazerRequisicao('/usuarios')

        if (componenteAtivo) {
          setUsuarios(dados)
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

    carregarUsuarios()

    return () => {
      componenteAtivo = false
    }
  }, [])

  function atualizarCampo(event) {
    const { name, value } = event.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  function abrirCadastro() {
    setUsuarioEditando(null)
    setFormulario(formularioInicial)
    setErroCadastro('')
    setMensagem('')
    setMostrarFormulario(true)
  }

  function abrirEdicao(item) {
    setUsuarioEditando(item.id)

    setFormulario({
      nome: item.nome,
      matricula: item.matricula,
      departamento: item.departamento,
      cargo: item.cargo,
      senha: '',
      confirmarSenha: '',
    })

    setErroCadastro('')
    setMensagem('')
    setMostrarFormulario(true)
  }

  function fecharFormulario() {
    setMostrarFormulario(false)
    setUsuarioEditando(null)
    setErroCadastro('')
    setFormulario(formularioInicial)
  }

  async function atualizarTabela() {
    const dados = await fazerRequisicao('/usuarios')
    setUsuarios(dados)
  }

  async function alterarStatusUsuario(item) {
    const acao = item.status ? 'desativar' : 'reativar'

    const confirmou = window.confirm(
      `Tem certeza de que deseja ${acao} o usuário ${item.nome}?`
    )

    if (!confirmou) {
      return
    }

    setErro('')
    setMensagem('')

    try {
      const endpoint = item.status
        ? `/usuarios/${item.id}`
        : `/usuarios/${item.id}/reativar`

      await fazerRequisicao(endpoint, {
        method: item.status ? 'DELETE' : 'PATCH',
      })

      setMensagem(
        item.status
          ? 'Usuário desativado com sucesso!'
          : 'Usuário reativado com sucesso!'
      )

      await atualizarTabela()
    } catch (erroRequisicao) {
      setErro(erroRequisicao.message)
    }
  }

  async function cadastrarUsuario(event) {
    event.preventDefault()

    setErroCadastro('')
    setMensagem('')

    const editando = usuarioEditando !== null

    if (!editando && formulario.senha.length < 12) {
      setErroCadastro('A senha deve possuir pelo menos 12 caracteres.')
      return
    }

    if (!editando && formulario.senha !== formulario.confirmarSenha) {
      setErroCadastro('As senhas não coincidem.')
      return
    }

    const dadosUsuario = {
      nome: formulario.nome.trim(),
      matricula: formulario.matricula.trim(),
      departamento: formulario.departamento.trim(),
      cargo: formulario.cargo.trim(),
    }

    if (!editando) {
      dadosUsuario.senha = formulario.senha
    }

    try {
      setSalvando(true)

      if (editando) {
        await fazerRequisicao(`/usuarios/${usuarioEditando}`, {
          method: 'PUT',
          body: JSON.stringify(dadosUsuario),
        })
      } else {
        await fazerRequisicao('/usuarios', {
          method: 'POST',
          body: JSON.stringify(dadosUsuario),
        })
      }

      await atualizarTabela()
      fecharFormulario()

      setMensagem(
        editando
          ? 'Usuário atualizado com sucesso!'
          : 'Usuário cadastrado com sucesso!'
      )
    } catch (erroRequisicao) {
      const detalhe = erroRequisicao.message

      setErroCadastro(
        typeof detalhe === 'string'
          ? detalhe
          : 'Dados inválidos. Verifique os campos e tente novamente.'
  )
    } finally {
      setSalvando(false)
    }
  }

  const usuariosFiltrados = usuarios.filter((item) => {
    const termo = pesquisa.toLowerCase()

    const correspondePesquisa =
      item.nome.toLowerCase().includes(termo) ||
      item.matricula.toLowerCase().includes(termo)

    const correspondeStatus =
      filtroStatus === 'todos' ||
      (filtroStatus === 'ativos' && item.status) ||
      (filtroStatus === 'inativos' && !item.status)

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

          <button className="navigation-item active" type="button">
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
            <span className="page-overline">GERENCIAMENTO</span>
            <h2>Usuários</h2>
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
              <h3>Usuários cadastrados</h3>
              <p>Consulte e filtre as identidades da plataforma.</p>
            </div>

            <div className="users-heading-actions">
              <span className="users-total">
                {usuarios.length} registros
              </span>

              <button
                className="new-user-button"
                type="button"
                onClick={abrirCadastro}
              >
                + Novo usuário
              </button>
            </div>
          </div>

          {mensagem && (
            <p className="users-success" role="status">
              {mensagem}
            </p>
          )}

          {mostrarFormulario && (
            <form className="user-form" onSubmit={cadastrarUsuario}>
              <h3>
                {usuarioEditando !== null
                  ? 'Editar usuário'
                  : 'Novo usuário'}
              </h3>

              <p>
                {usuarioEditando !== null
                  ? 'Altere os dados da identidade selecionada.'
                  : 'Preencha os dados para cadastrar uma nova identidade.'}
              </p>

              <div className="user-form-grid">
                <label>
                  Nome completo
                  <input
                    type="text"
                    name="nome"
                    value={formulario.nome}
                    onChange={atualizarCampo}
                    required
                  />
                </label>

                <label>
                  Matrícula
                  <input
                    type="text"
                    name="matricula"
                    value={formulario.matricula}
                    onChange={atualizarCampo}
                    required
                  />
                </label>

                <label>
                  Departamento
                  <input
                    type="text"
                    name="departamento"
                    value={formulario.departamento}
                    onChange={atualizarCampo}
                    required
                  />
                </label>

                <label>
                  Cargo
                  <input
                    type="text"
                    name="cargo"
                    value={formulario.cargo}
                    onChange={atualizarCampo}
                    required
                  />
                </label>

                {usuarioEditando === null && (
                  <>
                    <label>
                      Senha
                      <input
                        type="password"
                        name="senha"
                        value={formulario.senha}
                        onChange={atualizarCampo}
                        minLength={12}
                        autoComplete="new-password"
                        required
                      />
                    </label>

                    <label>
                      Confirmar senha
                      <input
                        type="password"
                        name="confirmarSenha"
                        value={formulario.confirmarSenha}
                        onChange={atualizarCampo}
                        minLength={12}
                        autoComplete="new-password"
                        required
                      />
                    </label>
                  </>
                )}
              </div>

              {usuarioEditando === null && (
                <p className="user-form-hint">
                  A senha deve possuir pelo menos 12 caracteres.
                </p>
              )}

              {erroCadastro && (
                <p className="users-error" role="alert">
                  {erroCadastro}
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
                    : usuarioEditando !== null
                      ? 'Salvar alterações'
                      : 'Cadastrar usuário'}
                </button>
              </div>
            </form>
          )}

          <div className="users-filters">
            <input
              type="search"
              placeholder="Pesquisar por nome ou matrícula..."
              value={pesquisa}
              onChange={(event) => setPesquisa(event.target.value)}
              aria-label="Pesquisar usuários"
            />

            <select
              value={filtroStatus}
              onChange={(event) => setFiltroStatus(event.target.value)}
              aria-label="Filtrar por status"
            >
              <option value="todos">Todos os status</option>
              <option value="ativos">Ativos</option>
              <option value="inativos">Inativos</option>
            </select>
          </div>

          {carregando && (
            <p className="users-feedback">Carregando usuários...</p>
          )}

          {!carregando && erro && (
            <p className="users-error" role="alert">
              {erro}
            </p>
          )}

          {!carregando && !erro && (
            <div className="users-table-container">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Matrícula</th>
                    <th>Departamento</th>
                    <th>Cargo</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>

                <tbody>
                  {usuariosFiltrados.map((item) => (
                    <tr key={item.id}>
                      <td>{item.nome}</td>
                      <td>{item.matricula}</td>
                      <td>{item.departamento}</td>
                      <td>{item.cargo}</td>
                      <td>
                        <span
                          className={`user-status ${
                            item.status ? 'active' : 'inactive'
                          }`}
                        >
                          {item.status ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td>
                        <div className="user-actions">
                          <button
                            className="edit-user-button"
                            type="button"
                            onClick={() => abrirEdicao(item)}
                          >
                            Editar
                          </button>

                          <button
                            className={
                              item.status
                                ? 'deactivate-user-button'
                                : 'activate-user-button'
                            }
                            type="button"
                            onClick={() => alterarStatusUsuario(item)}
                          >
                            {item.status ? 'Desativar' : 'Reativar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {usuariosFiltrados.length === 0 && (
                <p className="users-feedback">
                  Nenhum usuário encontrado.
                </p>
              )}
            </div>
          )}
        </section>
      </section>
    </main>
  )
}

export default Usuarios
