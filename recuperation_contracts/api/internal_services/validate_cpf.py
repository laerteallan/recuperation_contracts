LENGTH_CPF = 11
NUMBERS_STR = '1234567890'


class ValidateCPF:

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) != LENGTH_CPF:
            return False

        if cpf in (c * LENGTH_CPF for c in NUMBERS_STR):
            return False

        reverse_cpf = cpf[::-1]
        for i in range(2, 0, -1):
            enumerate_cpf = enumerate(reverse_cpf[i:], start=2)
            dv_calculado = sum(map(lambda x: int(x[1]) * x[0], enumerate_cpf)) * 10 % 11
            if reverse_cpf[i - 1:i] != str(dv_calculado % 10):
                return False
        return True
