-- Active: 1787099496149@@127.0.0.1@5432@bd_aula
CREATE TABLE curso(
    id_curso INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE aluno(
    id_aluno INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(80) NOT NULL, 
    id_curso INTEGER NOT NULL REFERENCES curso(id_curso)
);

SELECT * FROM curso;
SELECT * FROM aluno;

INSERT INTO curso (nome) VALUES 
('Sistemas de Informacao'),
('Administracao'),
('Direito'),
('Ciencias da Computacao');

INSERT INTO aluno (nome, id_curso) VALUES
('Ana Beatriz Souza', 1),
('Felipe Terra Alves Portella', 2),
('Gabriel Barbosa', 3),
('Giorgian de Arrascaeta', 1);

SELECT 
    id_aluno,
    nome, 
    id_curso 
FROM
    aluno
ORDER BY 
    id_aluno ASC;


SELECT table_name,
       column_name,
       data_type,
       character_maximum_length AS tamanho,
       is_nullable              AS aceita_nulo,
       is_identity              AS e_identidade
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('curso', 'aluno')
ORDER BY table_name, ordinal_position;


SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'curso';


SELECT 
    nome,  
    id_curso
FROM 
    aluno
WHERE
    id_curso = 1
ORDER BY
    nome DESC;



SELECT
    a.nome AS Aluno,
    c.nome AS Curso
FROM
        aluno a
    JOIN 
        curso c
    ON 
        c.id_curso = a.id_curso
ORDER BY 
    c.nome;



SELECT 
    c.nome AS curso,
    c.id_curso,
FROM
    curso c
WHERE
    c.nome = 'Sistemas de Informacao';


-- Quantos alunos tem em cada curso?

SELECT
    c.nome AS curso,
    COUNT(a.id_aluno) AS qtd_aluno
FROM 
    curso c
    JOIN
        aluno a
    ON 
        a.id_curso = c.id_curso
GROUP BY
    c.nome
ORDER BY
    qtd_aluno DESC;
    



