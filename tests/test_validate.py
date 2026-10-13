import unittest

import pandas as pd

from validate import validate


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'ispb': pd.Series(['00000000', '12345678'], dtype='string'),
            'name': pd.Series(['BANCO A', 'BANCO B'], dtype='string'),
            'code': pd.Series([1, pd.NA], dtype='Int64'),
            'full_name': pd.Series(['BANCO A S.A.', 'BANCO B S.A.'], dtype='string'),
        })

    def test_aceita_dados_validos_e_code_nulo(self):
        self.assertTrue(validate(self.df))

    def test_rejeita_ispb_duplicado(self):
        duplicados = pd.concat([self.df, self.df.iloc[[0]]], ignore_index=True)
        self.assertFalse(validate(duplicados))

    def test_rejeita_nome_ausente(self):
        dados = self.df.copy()
        dados.loc[0, 'name'] = pd.NA
        self.assertFalse(validate(dados))

    def test_rejeita_nome_completo_vazio(self):
        dados = self.df.copy()
        dados.loc[0, 'full_name'] = '   '
        self.assertFalse(validate(dados))

    def test_rejeita_coluna_ausente(self):
        self.assertFalse(validate(self.df.drop(columns=['code'])))


if __name__ == '__main__':
    unittest.main()
