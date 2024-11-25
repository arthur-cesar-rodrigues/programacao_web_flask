CREATE TABLE Arthur_tbusuario (
	codigo INT AUTO_INCREMENT PRIMARY Key,
	nome VARCHAR(80),
	email VARCHAR(50) unique,
	senha VARCHAR(30)
);



DROP TABLE Arthur_tbusuario;




SELECT codigo, nome, email, senha FROM Arthur_tbusuario


;




INSERT INTO Arthur_tbusuario (codigo, nome, email, senha) VALUES (1, "Margarida", "Margarida@gmail.com", "P@ssw0rd")

;

-- INSERT INTO Arthur_tbusuario (codigo) VALUES (3) -- inserindo apenas o valor de uma coluna, ou seja a linha vai ficar apenas com um valor verdadeiro e o resto com valores "null" 

-- INSERT INTO Arthur_tbusuario (codigo, nome, email, senha) VALUES (NULL, "Margarida", "Margarida@gmail.com", NULL) -- outra forma de inserir dados individuais, neste caso vamos inserir apenas dados de 2 colunas

SELECT codigo, nome, email, senha FROM Arthur_tbusuario 
WHERE -- Codigo = 3

; 
-- nome = "Margarida"
-- email = "Margarid3a@gmail.com" AND senha = "P@ssw0rd" (usando condição para encontrar um valor especifico)
-- email LIKE "Margarida%" -- pega todos os email que começarem com Margarida ou que vierem coisas depois
-- email LIKE "%Margarida%" -- pega todos os emails que vierem com coisas antes de Margarida ou vir depois, ou os dois juntos
email LIKE "Margar_da" -- procura todos os emails que possuirem dados entre aspas, e possuirem valores diferente aonde fica o underline


;
-- DELETE FROM Arthur_tbusuario -- comando para excluir todos os dados da tabela(linhas e colunas) ainda possibilita usar a tabela, diferente do drop que apaga a tabela
DELETE FROM  Arthur_tbusuario WHERE Codigo = 3

;
 -- deleta a linha onde for encontrado os dados que possuirem a lógica do where, é aconselhável usar o select daquela linha (usando o where) para se certificar e ver se o dado da linha que voce procura é realmente se o dado é o que precisa ser excluído
-- linha = é a menor unidade do banco de dados
-- em banco de dados não há espaço para erro (alteração, exlusão não tem mais volta), não deixe esses comandos de alterção na tela
-- UPDATE Arthur_tbusuario SET nome = "Rodrigo" -- update set = altera os dados de uma coluna de uma tabela; neste exemplo todos os dados da coluna nome são alterados para rodrigo; é recomendavel usar um where para alterar a o dado da linha em especifico que precisa ser alterada
-- UPDATE Arthur_tbusuario SET nome = "Rodrigo" WHERE codigo = 6 -- usando o where para alterar o dado de uma linha em especifico
UPDATE Arthur_tbusuario SET nome = "Rodrigo", codigo = 4 WHERE codigo = 6 -- alterando mais de um dado de uma linha, no caso esta sendo alterado os dados da coluna nome e codigo 



;








CREATE TABLE Arthur_exercicio (
	nome VARCHAR(80),
	cpf CHAR(14) PRIMARY KEY, 
	rg CHAR(13) UNIQUE,
	endereco VARCHAR(80),
	bairro VARCHAR(80),
	cidade VARCHAR(80),
	cep VARCHAR(50)
);

DROP TABLE Arthur_exercicio


SELECT * FROM Arthur_exercicio

;





CREATE TABLE Arthur_trabalho_disciplina (
	id INT AUTO_INCREMENT PRIMARY Key,
	nome VARCHAR(80),
	carga_horaria INT NOT NULL 
);


SELECT * FROM Arthur_trabalho_disciplina

;


DROP TABLE Arthur_trabalho_disciplina


;


CREATE TABLE Arthur_trabalho_curso (
	id INT AUTO_INCREMENT PRIMARY Key,
	nome VARCHAR(80) NOT NULL
);


SELECT * FROM Arthur_trabalho_curso


;



DROP TABLE Arthur_trabalho_curso


;



CREATE TABLE Arthur_trabalho_curso_disciplina (
	id INT AUTO_INCREMENT PRIMARY KEY,
	id_curso INT NOT NULL,
	id_disciplina INT NOT NULL,
	FOREIGN KEY (id_curso) REFERENCES Arthur_trabalho_curso(id),
	FOREIGN KEY (id_disciplina) REFERENCES Arthur_trabalho_disciplina(id)
);



SELECT * FROM Arthur_trabalho_curso_disciplina


;



DROP TABLE  Arthur_trabalho_curso_disciplina


;