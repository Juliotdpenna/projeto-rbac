import { useState } from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Usuarios from './pages/Usuarios'
import Roles from './pages/Roles'
import Permissoes from './pages/Permissoes'
import { limparAccessToken } from './services/api'
import Grupos from './pages/Grupos'

function App() {
  const [usuario, setUsuario] = useState(null)
  const [paginaAtual, setPaginaAtual] = useState('dashboard')

  function handleLogin(dadosUsuario) {
    setUsuario(dadosUsuario)
    setPaginaAtual('dashboard')
  }

  function handleLogout() {
    limparAccessToken()
    setUsuario(null)
    setPaginaAtual('dashboard')
  }

  if (!usuario) {
    return <Login onLogin={handleLogin} />
  }

  if (paginaAtual === 'usuarios') {
    return (
      <Usuarios
        usuario={usuario}
        onLogout={handleLogout}
        onNavigate={setPaginaAtual}
      />
    )
  }

  if (paginaAtual === 'roles') {
    return (
      <Roles
        usuario={usuario}
        onLogout={handleLogout}
        onNavigate={setPaginaAtual}
      />
    )
  }

  if (paginaAtual === 'permissoes') {
    return (
      <Permissoes
        usuario={usuario}
        onLogout={handleLogout}
        onNavigate={setPaginaAtual}
      />
    )
  }

  if (paginaAtual === 'grupos') {
    return (
      <Grupos
        usuario={usuario}
        onLogout={handleLogout}
        onNavigate={setPaginaAtual}
      />
    )
  }

  return (
    <Dashboard
      usuario={usuario}
      onLogout={handleLogout}
      onNavigate={setPaginaAtual}
    />
  )
}

export default App