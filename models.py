import datetime
class Cliente:
    def __init__(self, nome, cpf, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        
    def to_dict(self):
        return {"nome": self.nome, "cpf": self.cpf, "telefone": self.telefone, "email": self.email}
        
#Superclasse    
class Quarto:
    def __init__(self, numero, capacidade):
        self.numero = numero 
        self.capacidade = capacidade 
        self.comodidades = ["Ar condicionado, WI-FI, Serviço de Quarto, 2 camas de solteiro"]
        self.valor_diaria = 100.0 #valor normal
        
    def __str__(self):
        return f"Quarto {self.numero} - Diária: R$ {self.valor_diaria}"
    
    def to_dict(self):
        return {"numero": self.numero, "capacidade": self.capacidade, "valor_diaria": self.valor_diaria, "comodidades": self.comodidades, "tipo": "Quarto"}
        

class Suite(Quarto):
    def __init__(self, numero, capacidade):
          super().__init__(numero, capacidade)
          self.valor_diaria = 180.0 #valor da suite
          self.tem_hidromassagem = True
          self.tem_sala_de_estar = True
          
          self.comodidades = ["Ar Condicionado", "WI-FI", "Serviço de Quarto", "1 cama de casal"]
          
    def to_dict(self):
        dados = super().to_dict()
        dados["tipo"] = "Suite" # Sobrescreve o tipo
        return dados
        
class Reserva: 
    def __init__(self,
                 data_entrada, data_saida,quarto, cliente, status ,forma_pagamento):
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.quarto = quarto #associação de classe 
        self.cliente = cliente #associação de classe 
        self.status = status
        self.forma_pagamento = forma_pagamento
        self.valor_total = self.calcular_total()
        
    def calcular_total(self):
        d1 = datetime.datetime.strptime(self.data_entrada, "%d/%m/%Y")
        d2 = datetime.datetime.strptime(self.data_saida, "%d/%m/%Y")
        diferenca = d2 - d1 
        dias = diferenca.days
    
        valor_final = dias * self.quarto.valor_diaria
        
        return valor_final 
    
    def __str__(self):
        return f"Reserva do cliente {self.cliente.nome} no Quarto {self.quarto.numero} - Total: R$ {self.valor_total:.2f} - Status: {self.status}"
    
    def to_dict(self):
        return {
            "data_entrada": self.data_entrada,
            "data_saida": self.data_saida,
            "cliente": self.cliente.to_dict(), # Transforma o cliente aninhado
            "quarto": self.quarto.to_dict(),   # Transforma o quarto aninhado
            "status": self.status,
            "forma_pagamento": self.forma_pagamento,
            "valor_total": self.valor_total
        }