from database.conexao import conectar

def criar_tabelas(caminho_banco=None):
    conexao = conectar(caminho_banco)

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                departamento TEXT NOT NULL,
                cargo TEXT NOT NULL,
                status INTEGER NOT NULL CHECK (status IN (0, 1)),
                senha_hash TEXT 
            )
        """)

        colunas = [
            coluna[1]
            for coluna in cursor.execute(
                "PRAGMA table_info(usuarios)"
            ).fetchall()
        ]

        if "senha_hash" not in colunas:
            cursor.execute(
                "ALTER TABLE usuarios ADD COLUMN senha_hash TEXT"
            )

        cursor.execute("""
            SELECT
                COUNT(*) AS total_usuarios,
                SUM(CASE WHEN senha_hash IS NOT NULL OR senha_hash = '' THEN 1 ELSE 0 END) AS sem_hash
            FROM usuarios
        """)

        print(cursor.fetchone())

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT NOT NULL,
                status INTEGER NOT NULL CHECK (status IN (0, 1))
            )         
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS permissoes (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT NOT NULL,
                status INTEGER NOT NULL CHECK (status IN (0, 1))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grupos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT NOT NULL,
                status INTEGER NOT NULL CHECK (status IN (0, 1))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_roles (
                usuario_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (usuario_id, role_id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grupo_usuarios (
                grupo_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                PRIMARY KEY (grupo_id, usuario_id),
                FOREIGN KEY (grupo_id) REFERENCES grupos(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grupo_roles (
                grupo_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (grupo_id, role_id),
                FOREIGN KEY (grupo_id) REFERENCES grupos(id),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_permissoes (
                role_id INTEGER NOT NULL,
                permissao_id INTEGER NOT NULL,
                PRIMARY KEY (role_id, permissao_id),
                FOREIGN KEY (role_id) REFERENCES roles(id),
                FOREIGN KEY (permissao_id) REFERENCES permissoes(id)
            )
        """)

        conexao.commit()
        print("Tabelas criadas com sucesso.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabelas()
