from models.permissao import Permissao


def test_ativar_permissao_desativada():
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        False
    )

    permissao.ativar()

    assert permissao.status is True


def test_desativar_permissao_ativa():
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    permissao.desativar()

    assert permissao.status is False


def test_ativar_permissao_ja_ativa():
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    permissao.ativar()

    assert permissao.status is True


def test_desativar_permissao_ja_desativada():
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        False
    )

    permissao.desativar()

    assert permissao.status is False


def test_permissao_exibe_mensagem_ao_ativar_permissao_ja_ativa(capsys):
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    permissao.ativar()

    resultado = capsys.readouterr()

    assert "A permissão já está ativa." in resultado.out


def test_permissao_exibe_mensagem_ao_desativar_permissao_ja_desativada(capsys):
    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        False
    )

    permissao.desativar()

    resultado = capsys.readouterr()

    assert "A permissão já está desativada." in resultado.out
